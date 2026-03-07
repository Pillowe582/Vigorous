"""
URL configuration for Vigorous project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 认证相关路径必须在主应用之前注册
    path('', include('accounts.urls')),
    path('', include('web3d.urls')),
    
    # React 页面入口
    re_path(r'^menu/?$', TemplateView.as_view(template_name="index.html")),
    re_path(r'^explorer-.*$', TemplateView.as_view(template_name="index.html")),
    re_path(r'^project-editor/.*$', TemplateView.as_view(template_name="index.html")),
    re_path(r'^chess-editor/.*$', TemplateView.as_view(template_name="index.html")),
    # re_path(r'^.*$', TemplateView.as_view(template_name='index.html')), # 添加保底路由
]

# 开发环境下提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)