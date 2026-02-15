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

def editor(request):
    '''渲染编辑器页面，支持传入项目ID'''
    # 获取项目ID参数
    project_id = request.GET.get('project_id')
    project_data = None
    
    if project_id:
        try:
            # 获取项目对象
            project = get_object_or_404(ProjectModel, id=project_id)
            # 确保项目属于当前用户（如果是已登录用户）
            if request.user.is_authenticated and project.user != request.user:
                project = None
            else:
                # 准备项目数据供前端使用
                project_data = {
                    'id': project.id,
                    'name': project.name,
                    'description': project.description,
                    'parameters': project.parameters,
                    'status': project.status,
                    'created_at': project.created_at.strftime('%Y-%m-%d %H:%M:%S') if project.created_at else None,
                }
        except Exception as e:
            print(f"获取项目数据时出错: {e}")
            project_data = None
    
    # 将项目数据转换为JSON字符串传递给模板
    context = {
        'project_data': json.dumps(project_data, ensure_ascii=False) if project_data else 'null'
    }
    
    return render(request, 'web3d/editor.html', context)


@csrf_exempt
@login_required
def save_project(request):
    '''保存或更新项目信息API'''
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)
    
    try:
        # 解析POST数据
        data = json.loads(request.body.decode('utf-8'))
        
        project_id = data.get('projectId')
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        parameters = data.get('parameters', {})
        
        # 验证必要字段
        if not name:
            return JsonResponse({'error': '项目名称不能为空'}, status=400)
        
        user = request.user
        
        if project_id:
            # 更新现有项目
            try:
                project = ProjectModel.objects.get(id=project_id, user=user)
                project.name = name
                project.description = description
                project.parameters = parameters
                project.edited_at = timezone.now()
                project.save()
                
                response_data = {
                    'success': True,
                    'message': '项目更新成功',
                    'project_id': project.id,
                    'updated_at': project.edited_at.isoformat()
                }
            except ProjectModel.DoesNotExist:
                return JsonResponse({'error': '项目不存在或无权限访问'}, status=404)
        else:
            # 创建新项目
            project = ProjectModel.objects.create(
                name=name,
                description=description,
                parameters=parameters,
                user=user,
                status='draft'
            )
            
            response_data = {
                'success': True,
                'message': '项目创建成功',
                'project_id': project.id,
                'created_at': project.created_at.isoformat()
            }
            
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'保存失败: {str(e)}'}, status=500)


@csrf_exempt
@login_required
def delete_project(request):
    '''删除项目API'''
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)
    
    try:
        # 解析POST数据
        data = json.loads(request.body.decode('utf-8'))
        project_id = data.get('projectId')
        
        # 验证必要字段
        if not project_id:
            return JsonResponse({'error': '项目ID不能为空'}, status=400)
        
        user = request.user
        
        # 查找并删除项目
        try:
            project = ProjectModel.objects.get(id=project_id, user=user)
            project_name = project.name
            project.delete()
            
            response_data = {
                'success': True,
                'message': f'项目"{project_name}"删除成功'
            }
        except ProjectModel.DoesNotExist:
            return JsonResponse({'error': '项目不存在或无权限访问'}, status=404)
            
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'删除失败: {str(e)}'}, status=500)

@csrf_exempt
def test(request):
    # 返回一条成功接收的JSON响应
    response_data = {
        'status': 'success',
        'message': '请求已成功接收',
        'timestamp': timezone.now().isoformat()
    }
    return JsonResponse(response_data)
