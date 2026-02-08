from django.db import models

# Create your models here.
# web3d/models.py

from django.db import models
from django.contrib.auth.models import User

class DesignProject(models.Model):
    name = models.CharField(max_length=200, verbose_name="项目名称")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    edited_at = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    parameters = models.JSONField(default=dict, verbose_name="模型参数")
    stl_file = models.FileField(upload_to='generated_models/', blank=True, verbose_name="模型文件")
    preview_image = models.ImageField(upload_to='previews/', blank=True, verbose_name="预览图")
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', '草稿'),
            ('generating', '生成中'),
            ('completed', '已完成'),
            ('archived', '已归档'),
        ],
        default='draft',
        verbose_name="状态"
    )
    
    # 🆕 新增字段：项目描述
    description = models.TextField(blank=True, verbose_name="项目描述")  # 允许为空的文本字段

    def __str__(self):
        return f"{self.name} (by {self.user.username})" # 返回项目名

    class Meta:
        '''添加元数据'''
        ordering = ['-created_at']
        verbose_name = '设计项目'
        verbose_name_plural = '设计项目'