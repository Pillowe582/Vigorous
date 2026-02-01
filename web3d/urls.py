from django.urls import path
from . import views  # 从当前目录导入views模块

urlpatterns = [
    path('', views.hello_world, name='hello_world'),  # 将根路径映射到hello_world视图
]