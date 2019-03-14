from django.db import models
from official.models import Category, Keyword
from verify.models import User
# Create your models here.


class Tweet(models.Model):
    c = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='宠物科属')
    k = models.ForeignKey(to=Keyword, on_delete=models.CASCADE, verbose_name='宠物类别')
    a = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="作者", null=True)
    con = models.TextField(verbose_name='日常动态')
    img = models.ImageField(upload_to="upload/tweet/images", null=True,)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='发布日期')
    status = models.BooleanField(default=False, verbose_name="发布状态")
    pl_num = models.IntegerField(default=0, verbose_name='评论数')
    transpond = models.IntegerField(default=0, verbose_name='转发数')
    heart_num = models.IntegerField(default=0, verbose_name='点赞数')


# 评论表
class Comment(models.Model):
    con = models.TextField(verbose_name='评论的内容')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='发布日期')
    msg = models.ForeignKey(to=Tweet, on_delete=models.CASCADE, verbose_name='对应的动态')
    users = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='评论者')


# 点赞表
class Heart(models.Model):
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='点赞日期')
    u_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    msg = models.ForeignKey(to=Tweet, on_delete=models.CASCADE, verbose_name='对应的动态')
    users = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='点赞者')



