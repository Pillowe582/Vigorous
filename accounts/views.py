from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import re
from . import messages as amsg


class CaseInsensitiveAuthBackend(ModelBackend):
    """
    自定义认证后端，支持不区分大小写的用户名登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return None
        
        try:
            # 不区分大小写地查找用户
            user = User.objects.get(username__iexact=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            # 运行默认的检查以减少计时攻击
            User().set_password(password)
        
        return None


def validate_username_strict(username):
    """
    严格的用户名验证函数
    要求：只能包含字母、数字和@/./+/-/_，不能包含空格
    注意：保持原始大小写，不在这里转换为小写
    """
    if not username:
        raise ValueError('用户名不能为空')
    
    if len(username) > 150:
        raise ValueError('用户名长度不能超过150个字符')
    
    if ' ' in username:
        raise ValueError('用户名不能包含空格')
    
    # 允许字母、数字和@/./+/-/_
    if not re.match(r'^[a-zA-Z0-9@.+\-_]+$', username):
        raise ValueError('用户名只能包含字母、数字和@/./+/-/_字符')
    
    # 返回原始用户名，保持大小写
    return username


@login_required
def profile_view(request):
    if request.method == 'POST':
        # 获取表单数据
        new_username = request.POST.get('new_username', '').strip()
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        avatar = request.FILES.get('avatar')
        
        # 处理用户名修改
        if new_username and new_username != request.user.username:
            try:
                # 使用严格的用户名验证（保持原始大小写）
                validated_username = validate_username_strict(new_username)
                
                # 检查用户名是否已存在（不区分大小写）
                if User.objects.filter(username__iexact=validated_username).exclude(id=request.user.id).exists():
                    messages.error(request, '该用户名已被其他用户使用！')
                else:
                    old_username = request.user.username
                    request.user.username = validated_username  # 保持原始大小写存储
                    request.user.save()
                    messages.success(request, f'用户名已从 "{old_username}" 更新为 "{validated_username}"！')
            except Exception as e:
                messages.error(request, f'用户名不符合要求：{str(e)}')
        
        # 处理头像上传
        if avatar:
            request.user.profile.avatar = avatar
            request.user.profile.save()
            messages.success(request, '头像更新成功！')
        
        # 处理密码修改
        if new_password:
            if new_password != confirm_password:
                messages.error(request, '两次输入的密码不一致！')
            else:
                # 使用Django标准密码验证
                try:
                    from django.contrib.auth.password_validation import validate_password
                    validate_password(new_password, request.user)
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)  # 保持登录状态
                    messages.success(request, '密码修改成功！')
                except Exception as e:
                    messages.error(request, f'密码不符合要求：{str(e)}')
        
        # 如果没有任何修改，显示提示信息
        if not new_username and not avatar and not new_password:
            messages.info(request, '没有进行任何修改')
            
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() # AuthenticationForm 特有方法，直接获取验证成功的用户
            login(request, user)
            # 如果有 next 参数，跳转到原始请求页面；否则跳转到编辑器页面
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('web3d:home') 
        else:
            messages.error(request, amsg.LOGIN_FAILED)
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('web3d:home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            # 检查用户名是否已存在（不区分大小写）
            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, amsg.USERNAME_EXISTS.format(username=username))
                return render(request, 'accounts/register.html', {'form': form})
            
            # 检查邮箱是否已存在（如果有邮箱字段的话）
            email = form.cleaned_data.get('email', '')
            if email and User.objects.filter(email=email).exists():
                messages.error(request, amsg.EMAIL_EXISTS)
                return render(request, 'accounts/register.html', {'form': form})
            
            # 创建用户
            user = form.save()
            messages.success(request, amsg.REGISTRATION_SUCCESS.format(username=username))
            return redirect('accounts:login')
        else:
            messages.error(request, amsg.INVALID_FORM_DATA)
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

