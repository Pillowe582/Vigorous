from django.urls import path
from . import views  # 从当前目录导入views模块

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('editor/', views.editor, name='editor'),
    path('api/generator', views.generator_api, name='generator_api'),
]