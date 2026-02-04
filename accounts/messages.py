"""
账户相关的错误信息和成功消息定义
"""

# 注册相关消息
REGISTRATION_SUCCESS = '账户 {username} 创建成功!'
USERNAME_EXISTS = '用户名 "{username}" 已被注册，请选择其他用户名。'
EMAIL_EXISTS = '该邮箱地址已被注册。'
INVALID_FORM_DATA = '请检查表单数据并重新提交。'

# 登录相关消息
LOGIN_SUCCESS = "欢迎回来，{username}!"
LOGIN_FAILED = "用户名或密码错误，请重试。"
USER_NOT_EXISTS = "用户 '{username}' 不存在，请先注册。"
ALREADY_LOGGED_IN = "您已经登录了。"

# 登出相关消息
LOGOUT_SUCCESS = "您已成功退出登录!"

# 通用错误消息
GENERIC_ERROR = "发生未知错误，请稍后重试。"
PERMISSION_DENIED = "您没有权限执行此操作。"

# 表单验证错误
PASSWORD_MISMATCH = "两次输入的密码不匹配。"
PASSWORD_TOO_SHORT = "密码长度至少需要8个字符。"
USERNAME_INVALID = "用户名只能包含字母、数字和@/./+/-/_字符。"