from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import ProjectModel, PieceModel, TextureModel, PresetModel
from .serializers import (
    ProjectSerializer, 
    PieceSerializer, 
    TextureSerializer,
    PresetSerializer,
)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只有所有者才能修改自己的对象
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class ProjectViewSet(viewsets.ModelViewSet):
    """
    项目管理视图集
    提供项目创建、查询、更新、删除等完整API
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'edited_at', 'name']
    ordering = ['-edited_at']

    def get_queryset(self):
        # 只返回当前用户的项目，排除已删除的
        return ProjectModel.objects.filter(
            user=self.request.user
        ).select_related('user')

    

class PieceViewSet(viewsets.ModelViewSet):
    """
    棋子管理视图集
    支持项目筛选和详细信息查询
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['project', 'type']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'edited_at', 'name']
    ordering = ['-edited_at']
    def get_serializer_class(self):
        """
        动态选择序列化器：
        1. 访问列表(list)时，使用简略版。
        2. 访问详情(retrieve)或创建(create)等时，使用完整版。
        """
        if self.action == 'list':
            from .serializers import PieceListSerializer
            return PieceListSerializer
        return PieceSerializer

    def get_queryset(self):
        queryset = PieceModel.objects.filter(user=self.request.user)
        return queryset.select_related('project')

class TextureViewSet(viewsets.ModelViewSet):
    """
    纹理管理视图集
    支持纹理上传、查询、更新等操作
    """
    serializer_class = TextureSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['source']
    search_fields = ['name']
    ordering_fields = ['created_at', 'edited_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        return TextureModel.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
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
    filterset_fields = ['type']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'edited_at', 'name']
    ordering = ['-edited_at']

    def get_serializer_class(self):
        """
        动态选择序列化器：
        1. 访问列表(list)时，使用不依赖项目的简略版。
        2. 访问详情(retrieve)或创建(create)等时，使用完整版。
        """
        if self.action == 'list':
            from .serializers import PresetListSerializer
            return PresetListSerializer
        return PresetSerializer

    def get_queryset(self):
        return PresetModel.objects.filter(user=self.request.user)

    