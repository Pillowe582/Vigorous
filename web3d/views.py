from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import ProjectModel
from django.utils import timezone

# Create your views here.
def home(request):
    """项目首页的视图函数"""
    # 传递当前登录用户的用户名，如果没有登录则传递默认值
    username = request.user.username if request.user.is_authenticated else '访客'
    
    # 获取当前用户的项目列表（仅在用户已登录时）
    user_projects = None
    if request.user.is_authenticated:
        user_projects = ProjectModel.objects.filter(user=request.user).order_by('-edited_at')[:10]  # 获取最近的10个项目
    
    context = {
        'username': username, 
        'user': request.user,  # 传递完整的用户对象
        'user_projects': user_projects  # 传递用户的项目列表
    }
    return render(request, 'web3d/home.html', context)  # 渲染模板

def about(request):
    """关于页面的视图函数"""
    return HttpResponse('<h1>关于我们?</h1>')
def menu(request):
    return render(request, 'index.html')


@login_required
def get_current_user(request):
    """获取当前登录用户的信息"""
    return JsonResponse({
        'id':request.user.id,
        'username': request.user.username,
    })

@csrf_exempt
def test(request):
    # 返回一条成功接收的JSON响应
    response_data = {
        'status': 'success',
        'message': '请求已成功接收',
        'timestamp': timezone.now().isoformat()
    }
    return JsonResponse(response_data)
