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
    PresetSerializer
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
    serializer_class = PieceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['project_id', 'type']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'edited_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = PieceModel.objects.filter(user=self.request.user)
        
        # 支持通过url参数过滤项目下的棋子
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
            
        return queryset.select_related('project_id', 'preset')

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
    支持预设的创建、查询、分享等功能
    """
    serializer_class = PresetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'edited_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        return PresetModel.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """复制预设为新的棋子"""
        preset = self.get_object()
        # 创建新的棋子实例
        piece_data = {
            'name': f"{preset.name}_副本",
            'description': preset.description,
            'parts': preset.parts,
            'feature': preset.feature,
            'piece_tags': preset.piece_tags,
            'preset': preset.id,
            'project_id': request.data.get('project_id')  # 需要指定项目ID
        }
        
        serializer = PieceSerializer(data=piece_data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)