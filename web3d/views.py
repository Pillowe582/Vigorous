from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ProjectModel
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.conf import settings
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

@login_required
def menu(request):
    """模型编辑器页面 - 需要登录访问"""
    return render(request, 'index.html')


@login_required
def get_current_user(request):
    """获取当前登录用户的信息"""
    return JsonResponse({
        'id':request.user.id,
        'username': request.user.username,
    })
    
@api_view(['POST'])
@csrf_exempt
def fetchLLM(request):
    # 获取前端传递的参数
    prompt = request.data.get('prompt')
    messages = request.data.get('messages')
    
    try:
        # 如果前端直接传递了 messages 数组，优先使用
        if messages and isinstance(messages, list):
            request_messages = messages
        else:
            # 否则使用默认的 messages 格式（只有用户消息）
            request_messages = [
                {"role": "user", "content": prompt}
            ]
        
        res = requests.post(
            settings.API_URL,
            headers={
                "Authorization": f"Bearer {settings.API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.API_MODEL,
                "messages": request_messages,
            },
        )

        data = res.json()
        reply = data["choices"][0]["message"]["content"]

        return Response({"reply": reply})

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@csrf_exempt
def test(request):
    # 返回一条成功接收的JSON响应
    response_data = {
        'status': 'success',
        'message': '请求已成功接收',
        'timestamp': timezone.now().isoformat()
    }
    return JsonResponse(response_data)


