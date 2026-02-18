# web3d/admin.py

from django.contrib import admin
from .models import ProjectModel, PresetModel, PieceModel, TextureModel

admin.site.site_header = "3D模型生成器管理后台"
admin.site.site_title = "3D生成器管理"
admin.site.index_title = "欢迎使用3D模型生成器管理系统"

# 注册项目模型
@admin.register(ProjectModel)
class ProjectModelAdmin(admin.ModelAdmin):
    # 在列表页显示的字段
    list_display = ('id','name', 'user', 'created_at', 'status')
    
    # 可搜索的字段
    search_fields = ('name', 'description', 'user__username')
    
    # 右侧过滤器
    list_filter = ('status', 'created_at', 'user')
    
    # 按创建时间降序排列
    ordering = ('-created_at',)
    
    # 只读字段（创建后不可编辑）
    readonly_fields = ('created_at', 'edited_at')
    
    # 每页显示数量
    list_per_page = 20
    
    # 字段分组显示
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'user', 'status', 'description')
        }),
        ('参数与时间', {
            'fields': ('feature', 'project_tags', 'created_at', 'edited_at'),
            'classes': ('collapse',)  # 可折叠
        }),
    )

# 注册预设棋子模型
@admin.register(PresetModel)
class PresetModelAdmin(admin.ModelAdmin):
    # 在列表页显示的字段
    list_display = ('id','name', 'user', 'type', 'created_at')
    
    # 可搜索的字段
    search_fields = ('name', 'description', 'user__username')
    
    # 右侧过滤器
    list_filter = ('type', 'created_at', 'user')
    
    # 按创建时间降序排列
    ordering = ('-created_at',)
    
    # 只读字段
    readonly_fields = ('created_at', 'edited_at')
    
    # 每页显示数量
    list_per_page = 20
    
    # 字段分组显示
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'user', 'type', 'description')
        }),
        ('设计参数', {
            'fields': ('parts', 'feature', 'piece_tags'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'edited_at'),
            'classes': ('collapse',)
        }),
    )

# 注册项目棋子模型
@admin.register(PieceModel)
class PieceModelAdmin(admin.ModelAdmin):
    # 在列表页显示的字段
    list_display = ('id','name', 'user', 'project', 'type', 'created_at')
    
    # 可搜索的字段
    search_fields = ('name', 'description', 'user__username', 'project__name')
    
    # 右侧过滤器
    list_filter = ('type', 'created_at', 'user', 'project')
    
    # 按创建时间降序排列
    ordering = ('-created_at',)
    
    # 只读字段
    readonly_fields = ('created_at', 'edited_at')
    
    # 每页显示数量
    list_per_page = 20
    
    # 字段分组显示
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'user', 'project', 'type', 'description')
        }),
        ('设计参数', {
            'fields': ('parts', 'feature', 'piece_tags'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'edited_at'),
            'classes': ('collapse',)
        }),
    )

# 注册纹理模型
@admin.register(TextureModel)
class TextureModelAdmin(admin.ModelAdmin):
    # 在列表页显示的字段
    list_display = ('id','name', 'user', 'source', 'created_at')
    
    # 可搜索的字段
    search_fields = ('name', 'user__username')
    
    # 右侧过滤器
    list_filter = ('source', 'created_at', 'user')
    
    # 按创建时间降序排列
    ordering = ('-created_at',)
    
    # 只读字段
    readonly_fields = ('created_at', 'edited_at')
    
    # 每页显示数量
    list_per_page = 20
    
    # 字段分组显示
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'user', 'file', 'source')
        }),
        ('纹理参数', {
            'fields': ('texture_tags', 'composition'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'edited_at'),
            'classes': ('collapse',)
        }),
    )