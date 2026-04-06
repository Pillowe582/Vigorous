from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.db import transaction
from datetime import datetime
import copy

from .models import (
    ProjectModel,
    PieceModel,
    TextureModel,
    PresetModel,
    TemplateModel,
    DecorationModel,
)
from .serializers import (
    ProjectSerializer,
    PieceSerializer,
    TextureSerializer,
    PresetSerializer,
    TemplateSerializer,
    DecorationSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只有所有者才能修改自己的对象
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class ProjectViewSet(viewsets.ModelViewSet):
    """
    项目管理视图集
    提供项目创建、查询、更新、删除等完整 API
    """

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "edited_at", "name"]
    ordering = ["-edited_at"]

    def get_queryset(self):
        # 只返回当前用户的项目，排除已删除的
        return ProjectModel.objects.filter(user=self.request.user).select_related(
            "user"
        )

    @action(detail=False, methods=["get"])
    def all_tags(self, request):
        """
        获取当前用户所有项目的所有唯一标签
        """
        # 获取当前用户的所有项目
        projects = ProjectModel.objects.filter(user=request.user).only("project_tags")

        # 收集所有标签
        all_tags = set()
        for project in projects:
            if project.project_tags:
                all_tags.update(project.project_tags)

        # 转换为排序后的列表返回
        return Response(sorted(list(all_tags)))


class PieceViewSet(viewsets.ModelViewSet):
    """
    棋子管理视图集
    支持项目筛选和详细信息查询
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["project", "type"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "edited_at", "name"]
    ordering = ["-edited_at"]

    def get_serializer_class(self):
        """
        动态选择序列化器：
        1. 访问列表(list)时，使用简略版。
        2. 访问详情(retrieve)或创建(create)等时，使用完整版。
        """
        if self.action == "list":
            from .serializers import PieceListSerializer

            return PieceListSerializer
        return PieceSerializer

    def get_queryset(self):
        queryset = PieceModel.objects.filter(user=self.request.user)
        return queryset.select_related("project")

    @action(detail=True, methods=["post"])
    def save_as_preset(self, request, pk=None):
        """
        将棋子保存为私有预设模板
        POST /api/pieces/{id}/save_as_preset/
        请求体: { "name": "preset name", "description": "preset description" (optional) }
        """
        piece = self.get_object()

        # 验证用户权限（使用 user_id 比较，避免对象比较在某些场景下误判）
        request_user_id = getattr(request.user, "id", None)
        if piece.user_id != request_user_id:
            return Response(
                {
                    "error": "你没有权限保存别人的棋子",
                    "debug": {
                        "piece_user_id": piece.user_id,
                        "request_user_id": request_user_id,
                    },
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # 获取请求数据
        name = request.data.get("name", f"{piece.name} (Preset)")
        description = request.data.get("description", piece.description)

        # 验证名称
        if not name or len(name.strip()) == 0:
            return Response(
                {"error": "预设名称不能为空"}, status=status.HTTP_400_BAD_REQUEST
            )

        if len(name) > 200:
            return Response(
                {"error": "预设名称不能超过200字符"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 深拷贝棋子数据到预设
        try:
            preset = PresetModel.objects.create(
                user=request.user,
                name=name,
                description=description,
                parts=copy.deepcopy(piece.parts),
                type=piece.type,
                feature=copy.deepcopy(piece.feature),
                piece_tags=copy.deepcopy(piece.piece_tags),
                is_public=False,  # 默认私有
            )

            from .serializers import PresetSerializer

            serializer = PresetSerializer(preset, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": f"保存预设失败: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )


class TextureViewSet(viewsets.ModelViewSet):
    """
    纹理管理视图集
    支持纹理上传、查询、更新等操作
    """

    serializer_class = TextureSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["created_at", "edited_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return TextureModel.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        重写 update 方法，支持 multipart/form-data 的 PATCH 请求
        """
        partial = kwargs.get("partial", True)
        instance = self.get_object()

        # 如果是 multipart/form-data，需要特殊处理
        if request.content_type.startswith("multipart/form-data"):
            # 合并 request.data 和 request.FILES
            from django.http import QueryDict

            data = (
                request.data.copy()
                if hasattr(request.data, "copy")
                else dict(request.data)
            )

            # 将文件添加到数据中
            for key, file in request.FILES.items():
                data[key] = file

            serializer = self.get_serializer(instance, data=data, partial=partial)
        else:
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def upload(self, request):
        """专门的纹理上传接口"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DecorationViewSet(viewsets.ModelViewSet):
    """
    装饰管理视图集
    支持装饰上传、查询、更新等操作
    """

    serializer_class = DecorationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["created_at", "edited_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return DecorationModel.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def upload(self, request):
        """专门的纹理上传接口"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PresetViewSet(viewsets.ModelViewSet):
    """
    预设棋子管理视图集
    支持预设的创建、查询、分享、转换为项目棋子等功能
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["type"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "edited_at", "name"]
    ordering = ["-edited_at"]

    def get_serializer_class(self):
        """
        动态选择序列化器：
        1. 访问列表(list)时，使用不依赖项目的简略版。
        2. 访问详情(retrieve)或创建(create)等时，使用完整版。
        """
        if self.action == "list":
            from .serializers import PresetListSerializer

            return PresetListSerializer
        return PresetSerializer

    def get_queryset(self):
        return PresetModel.objects.filter(Q(user=self.request.user) | Q(is_public=True))

    def perform_create(self, serializer):
        # 仅管理员可通过 API 创建公开预设，普通用户提交时强制为私有。
        is_public = serializer.validated_data.get("is_public", False)
        if is_public and not self.request.user.is_staff:
            serializer.save(user=self.request.user, is_public=False)
            return
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # 仅管理员可通过 API 修改公开状态。
        if "is_public" in serializer.validated_data and not self.request.user.is_staff:
            serializer.save(is_public=serializer.instance.is_public)
            return
        serializer.save()

    @action(detail=True, methods=["post"])
    def apply_to_projects(self, request, pk=None):
        """
        将预设应用到指定项目，或自动创建新项目
        POST /api/presets/{id}/apply_to_projects/
        请求体: {
            "project_ids": [1, 2, 3] (optional, 空则自动创建项目)
            "piece_name": "custom piece name" (optional)
        }
        返回: {
            "created_pieces": [...],
            "created_project": {...} or null,
            "failed_projects": [...],
            "message": "success message"
        }
        """
        preset = self.get_object()

        # 验证用户权限（只能申请公开预设或自己的预设）
        if preset.user != request.user and not preset.is_public:
            return Response(
                {"error": "你没有权限申请此预设"}, status=status.HTTP_403_FORBIDDEN
            )

        project_ids = request.data.get("project_ids", [])
        piece_name = request.data.get("piece_name", preset.name)

        # 验证piece_name
        if not piece_name or len(piece_name.strip()) == 0:
            return Response(
                {"error": "棋子名称不能为空"}, status=status.HTTP_400_BAD_REQUEST
            )

        if len(piece_name) > 200:
            return Response(
                {"error": "棋子名称不能超过200字符"}, status=status.HTTP_400_BAD_REQUEST
            )

        created_pieces = []
        created_project_data = None
        failed_projects = []

        try:
            with transaction.atomic():
                # 如果没有提供项目ID，自动创建新项目
                if not project_ids or len(project_ids) == 0:
                    project_name = (
                        f"从模板创建-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                    )
                    try:
                        created_project = ProjectModel.objects.create(
                            user=request.user,
                            name=project_name,
                            description=f"从预设 '{preset.name}' 创建",
                            feature=copy.deepcopy(preset.feature),
                            project_tags=[],
                        )
                        project_ids = [created_project.id]
                        created_project_data = {
                            "id": created_project.id,
                            "name": created_project.name,
                            "description": created_project.description,
                        }
                    except Exception as e:
                        return Response(
                            {"error": f"自动创建项目失败: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                # 验证所有项目都属于当前用户
                user_projects = ProjectModel.objects.filter(
                    user=request.user, id__in=project_ids
                ).values_list("id", flat=True)

                invalid_project_ids = set(project_ids) - set(user_projects)
                if invalid_project_ids:
                    return Response(
                        {
                            "error": f"以下项目不存在或不属于你: {list(invalid_project_ids)}"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # 为每个项目创建棋子
                for project_id in project_ids:
                    try:
                        project = ProjectModel.objects.get(
                            id=project_id, user=request.user
                        )
                        piece = PieceModel.objects.create(
                            user=request.user,
                            name=piece_name,
                            description=f"从预设 '{preset.name}' 导入",
                            parts=copy.deepcopy(preset.parts),
                            type=preset.type,
                            feature=copy.deepcopy(preset.feature),
                            piece_tags=copy.deepcopy(preset.piece_tags),
                            project=project,
                        )

                        from .serializers import PieceSerializer

                        piece_serializer = PieceSerializer(
                            piece, context={"request": request}
                        )
                        created_pieces.append(piece_serializer.data)
                    except Exception as e:
                        failed_projects.append(
                            {"project_id": project_id, "error": str(e)}
                        )

            # 构建返回数据
            response_data = {
                "created_pieces": created_pieces,
                "created_project": created_project_data,
                "failed_projects": failed_projects,
                "message": f"成功在 {len(created_pieces)} 个项目中应用预设"
                + (
                    f"，自动创建项目 '{created_project_data['name']}'"
                    if created_project_data
                    else ""
                ),
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"应用预设失败: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )


class TemplateViewSet(viewsets.ModelViewSet):
    """
    模板棋子管理视图集
    支持项目筛选和详细信息查询
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["project", "type"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "edited_at", "name"]
    ordering = ["-edited_at"]

    def get_serializer_class(self):
        """
        动态选择序列化器：
        1. 访问列表(list)时，使用简略版。
        2. 访问详情(retrieve)或创建(create)等时，使用完整版。
        """
        if self.action == "list":
            from .serializers import TemplateListSerializer

            return TemplateListSerializer
        return TemplateSerializer

    def get_queryset(self):
        queryset = TemplateModel.objects.filter(user=self.request.user)
        return queryset.select_related("project")
