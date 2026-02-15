from django.db import models

# Create your models here.
# web3d/models.py

from django.db import models
from django.contrib.auth.models import User

class BasicInfoModel(models.Model):
    '''这里是每个数据库都要继承的基本模型'''
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    edited_at = models.DateTimeField(auto_now=True,verbose_name="修改时间")
    name = models.CharField(max_length=200, verbose_name="名称")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)s", verbose_name="创建者")

    class Meta:
        abstract = True # 抽象模型，不会生成表

class ProjectModel(BasicInfoModel):
    """项目模型：包含多个棋子的一个大项目"""
    description = models.TextField(blank=True, verbose_name="项目描述") 
    feature = models.JSONField(default=lambda:{"shape":"square","size":10}, verbose_name="基本单位形状")
    project_tags = models.JSONField(default=list, blank=True, verbose_name="标签集合")
    status = models.CharField(
        max_length=20,
        choices=[
            ('editable', '可编辑'),
            ('protected', '锁定'),
            ('archived', '已归档'),
        ],
        default='editable',
        verbose_name="项目状态"
    )
    
    
    def __str__(self):
        return f"{self.user.username}的项目：{self.name}" # 直接打印对象时，返回项目名

    class Meta:
        '''添加元数据'''
        ordering = ['-created_at']
        verbose_name = '设计项目'
        verbose_name_plural = '设计项目'
        
class PieceAbstract(BasicInfoModel):
    '''棋子抽象类'''
    description=models.TextField(blank=True, verbose_name="棋子描述")
    parts=models.JSONField(default=dict, verbose_name="棋子设计格式")  
    type=models.CharField(max_length=20, choices=[('default', '普通')], default='default', verbose_name="棋子类型")
    feature=models.JSONField(default=lambda:{"shape":"square","size":10}, verbose_name="此棋子形状")
    piece_tags=models.JSONField(default=list, blank=True, verbose_name="棋子标签")
    
    class Meta:
        abstract = True
        
class PresetModel(PieceAbstract):
    """预设棋子模型"""
    def __str__(self):
        return f"{self.user.username}的预设棋子：{self.name}" 
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '预设棋子'
        verbose_name_plural = '预设棋子'
        
class PieceModel(PieceAbstract):
    '''项目下的一个棋子'''
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE, verbose_name="所属项目")
    
    def __str__(self):
        return f"{self.user.username}的项目{self.project.name}下的棋子：{self.name}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '项目下的棋子'
        verbose_name_plural = '项目下的棋子'
        
class TextureModel(BasicInfoModel):
    """纹理模型"""
    file=models.ImageField(upload_to='textures/', verbose_name="纹理图片")
    texture_tags=models.JSONField(default=list, blank=True, verbose_name="纹理标签")
    source=models.CharField(max_length=200,choices=[('upload','上传'),('composite','合成')], blank=True, verbose_name="纹理来源")
    composition=models.JSONField(default=dict, blank=True, verbose_name="纹理合成格式")
    def __str__(self):
        return f"{self.user.username}的纹理：{self.name}"
    class Meta:
        ordering = ['-created_at']
        verbose_name = '纹理'
        verbose_name_plural = '纹理'
        
