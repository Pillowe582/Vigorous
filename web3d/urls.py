from django.urls import path
from . import views  # 从当前目录导入views模块

app_name = 'web3d'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('editor/', views.editor, name='editor'),
    path('api/save-project/', views.save_project, name='save_project'),
    path('api/delete-project/', views.delete_project, name='delete_project'),
    path('api/test/', views.test, name='test')
]