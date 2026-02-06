from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import DesignProject
import json

# Create your views here.
def home(request):
    """项目首页的视图函数"""
    # 传递当前登录用户的用户名，如果没有登录则传递默认值
    username = request.user.username if request.user.is_authenticated else '访客'
    
    # 获取当前用户的项目列表（仅在用户已登录时）
    user_projects = None
    if request.user.is_authenticated:
        user_projects = DesignProject.objects.filter(user=request.user).order_by('-created_at')[:10]  # 获取最近的10个项目
    
    context = {
        'username': username, 
        'user': request.user,  # 传递完整的用户对象
        'user_projects': user_projects  # 传递用户的项目列表
    }
    return render(request, 'web3d/home.html', context)  # 渲染模板

def about(request):
    """关于页面的视图函数"""
    return HttpResponse('<h1>关于我们?</h1>')

def editor(request):
    '''渲染静态文件目录下的index.html文件。似乎无法直接使用render()函数，因为index.html文件在静态文件目录下，
    而render()函数默认从模板目录下渲染文件。AI推荐使用django.views.static.serve()函数来渲染静态文件。'''
    from django.views.static import serve
    import os
    from django.conf import settings
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'index.html')
    return serve(request, os.path.basename(file_path), os.path.dirname(file_path))
    
'''先前代码，先注释掉
def generator_api(request):
    """API接口：接收前端发送的参数，返回处理结果（暂为模拟）"""
    if request.method == "POST":
        # 1. 接收前端通过POST请求发送的JSON数据
        try:
            data = json.loads(request.body)
            thickness = data.get('thickness')
            pattern = data.get('pattern')
            # ... 获取其他参数
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})

        # 2. （模拟）处理数据：这里是未来3D生成算法的位置
        # 目前先简单地将参数原样返回，确保通信畅通
        response_data = {
            'status': 'success',
            'message': f'收到参数！厚度：{thickness}，图案：{pattern}。3D模型生成功能待实现。',
            'received_params': data  # 将收到的数据返回给前端，用于调试
        }

        # 3. 返回JSON响应
        return JsonResponse(response_data)
    else:
        # 如果不是POST请求，返回错误
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
'''