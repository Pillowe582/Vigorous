from django.db import models
from django.core.validators import FileExtensionValidator
import os
from datetime import datetime

# Create your models here.
# web3d/models.py

from django.db import models
from django.contrib.auth.models import User


def get_default_feature():
    return {"shape": "square", "size": 10}


class BasicInfoModel(models.Model):
    """这里是每个数据库都要继承的基本模型"""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    edited_at = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    name = models.CharField(max_length=200, verbose_name="名称")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s", verbose_name="创建者"
    )

    class Meta:
        abstract = True  # 抽象模型，不会生成表


class ProjectModel(BasicInfoModel):
    """项目模型：包含多个棋子的一个大项目"""

    description = models.TextField(blank=True, verbose_name="项目描述")
    feature = models.JSONField(default=get_default_feature, verbose_name="基本单位形状")
    project_tags = models.JSONField(default=list, blank=True, verbose_name="标签集合")
    status = models.CharField(
        max_length=20,
        choices=[
            ("editable", "可编辑"),
            ("protected", "锁定"),
            ("archived", "已归档"),
        ],
        default="editable",
        verbose_name="项目状态",
    )

    def __str__(self):
        return f"{self.user.username}的项目：{self.name}"  # 直接打印对象时，返回项目名

    class Meta:
        """添加元数据"""

        ordering = ["-created_at"]
        verbose_name = "设计项目"
        verbose_name_plural = "设计项目"


class PieceAbstract(BasicInfoModel):
    """棋子抽象类"""

    description = models.TextField(blank=True, verbose_name="棋子描述")
    parts = models.JSONField(default=dict, verbose_name="棋子设计格式")
    type = models.CharField(
        max_length=20,
        choices=[("default", "普通")],
        default="default",
        verbose_name="棋子类型",
    )
    feature = models.JSONField(default=get_default_feature, verbose_name="此棋子形状")
    piece_tags = models.JSONField(default=list, blank=True, verbose_name="棋子标签")

    class Meta:
        abstract = True


class PresetModel(PieceAbstract):
    """预设棋子模型"""

    is_public = models.BooleanField(
        default=False,
        verbose_name="所有已登录用户可见",
        help_text="勾选后，所有已登录用户都可以查看此预设棋子。",
    )

    def __str__(self):
        return f"{self.user.username}的预设棋子：{self.name}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "预设棋子"
        verbose_name_plural = "预设棋子"


class PieceModel(PieceAbstract):
    """项目下的一个棋子"""

    project = models.ForeignKey(
        ProjectModel, on_delete=models.CASCADE, verbose_name="所属项目"
    )

    def __str__(self):
        return f"{self.user.username}的项目{self.project.name}下的棋子：{self.name}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "项目下的棋子"
        verbose_name_plural = "项目下的棋子"


class TemplateModel(PieceAbstract):
    """模板棋子模型"""

    project = models.ForeignKey(
        ProjectModel, on_delete=models.CASCADE, verbose_name="所属项目"
    )

    def __str__(self):
        return f"{self.user.username}的模板：{self.name}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "模板棋子"
        verbose_name_plural = "模板棋子"


def file_upload_path(instance, filename):
    """
    自定义纹理图片上传路径
    文件名格式：用户名_时间戳.扩展名
    """
    # 获取文件扩展名
    ext = os.path.splitext(filename)[1][1:]  # 去掉点号
    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 构建文件名：用户名_时间戳。扩展名
    new_filename = (
        f"{instance.user.username}/{ext}/{instance.user.username}_{timestamp}.{ext}"
    )
    # 返回完整路径：userassets/用户名_时间戳.扩展名
    return os.path.join("userassets", new_filename)


class TextureModel(BasicInfoModel):
    """纹理模型"""

    file = models.ImageField(
        upload_to=file_upload_path,
        verbose_name="纹理图片",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg", "webp"])],
    )
    texture_tags = models.JSONField(default=list, blank=True, verbose_name="纹理标签")

    def __str__(self):
        return f"{self.user.username}的纹理：{self.name}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "纹理"
        verbose_name_plural = "纹理"


class DecorationModel(BasicInfoModel):
    """装饰模型"""

    file = models.FileField(
        upload_to=file_upload_path,
        verbose_name="装饰文件",
        validators=[FileExtensionValidator(["stl", "obj"])],
    )
    decoration_tags = models.JSONField(
        default=list, blank=True, verbose_name="装饰标签"
    )

    def __str__(self):
        return f"{self.user.username}的装饰：{self.name}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "装饰"
        verbose_name_plural = "装饰"
