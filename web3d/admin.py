# generator/admin.py

from django.contrib import admin
from .models import DesignProject

admin.site.site_header = "3D模型生成器管理后台"
admin.site.site_title = "3D生成器管理"
admin.site.index_title = "欢迎使用3D模型生成器管理系统"

# 方式2：使用装饰器注册（推荐，更灵活）
@admin.register(DesignProject)
class DesignProjectAdmin(admin.ModelAdmin):
    # 在列表页显示的字段
    list_display = ('name', 'user', 'created_at', 'status')
    
    # 可搜索的字段
    search_fields = ('name', 'description')
    
    # 右侧过滤器
    list_filter = ('status', 'created_at', 'user')
    
    # 按创建时间降序排列
    ordering = ('-created_at',)
    
    # 只读字段（创建后不可编辑）
    readonly_fields = ('created_at',)
    
    # 每页显示数量
    list_per_page = 20
    
    # 字段分组显示
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'user', 'status', 'description')
        }),
        ('参数与时间', {
            'fields': ('parameters', 'created_at'),
            'classes': ('collapse',)  # 可折叠
        }),
        ('文件', {
            'fields': ('stl_file', 'preview_image')
        }),
    )