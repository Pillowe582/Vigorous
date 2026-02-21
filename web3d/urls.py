from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  # 从当前目录导入views模块
from . import views_api  # 导入API视图

app_name = 'web3d'

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'api/projects', views_api.ProjectViewSet, basename='project')
router.register(r'api/pieces', views_api.PieceViewSet, basename='piece')
router.register(r'api/textures', views_api.TextureViewSet, basename='texture')
router.register(r'api/presets', views_api.PresetViewSet, basename='preset')

urlpatterns = [
    # 传统页面路由
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('editor/', views.editor, name='editor'),
    path("api/getuser/", views.get_current_user, name="getuser"),
    
    
    
    # REST API路由
    path('', include(router.urls)),
]