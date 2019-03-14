from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=12, default='', null=True, error_messages={"required": "用户名不能为空", })
    password = models.CharField(max_length=16, error_messages={"required": "密码不能为空", })
    email = models.EmailField()
    tel = models.CharField(max_length=13, validators=[
        RegexValidator(regex=r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$', message='手机号格式不对吧！')
    ])
    img = models.ImageField(upload_to="upload/user_msg/images")
    flower = models.TextField(max_length=65535, default='')
    star = models.TextField(max_length=65535, default='')
    cate = models.CharField(max_length=16, verbose_name='宠物科属')
    key = models.CharField(max_length=16, verbose_name='宠物品种')

    def __str__(self):
        return self.username


