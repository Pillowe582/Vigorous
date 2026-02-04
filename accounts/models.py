
# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField("昵称", max_length=50, blank=True)
    avatar = models.ImageField("头像", upload_to="avatars/", blank=True, null=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} 的个人资料"

# 信号：用户创建时自动生成 Profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # 使用 get_or_create 更加安全，防止重复创建报错
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # 先检查是否有 profile 属性，避免 RelatedObjectDoesNotExist 错误
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # 如果保存时发现漏了 Profile（比如你刚才遇到的情况），自动补齐
        Profile.objects.get_or_create(user=instance)