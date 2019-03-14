from django.forms import ModelForm, Widget
from django import forms
from .models import User
from captcha.fields import CaptchaField
from django.core.validators import ValidationError


class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "inputs", "placeholder": "请输入密码", "value": "", "required": "required", }),
                               min_length=6, max_length=16, error_messages={"required": "密码不能为空", })

    class Meta:
        model = User
        exclude = ['img', 'flower', 'star', 'cate', 'key']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'inputs',
                'placeholder': '请输入用户名'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'inputs',
                'placeholder': '请输入密码'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'inputs',
                'placeholder': '请输入邮箱'
            }),
            'tel': forms.TextInput(attrs={
                'class': 'inputs',
                'placeholder': '请输入手机号'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        tel = cleaned_data.get('tel', None)
        email = cleaned_data.get('email', None)
        print(tel, email)
        if tel and email:
            is_tel_exist = User.objects.filter(tel=tel).first()
            is_email_exist = User.objects.filter(email=email).first()
            if is_email_exist and is_tel_exist:
                raise ValidationError('该手机号和邮箱都已被人注册过了')
            if is_email_exist:
                raise ValidationError('该邮箱已被人注册过了')
            if is_tel_exist:
                raise ValidationError('该手机号已被人注册过了')


class LoginForm(ModelForm):
    # captcha = CaptchaField()    # django自带的图片验证

    class Meta:
        model = User
        exclude = ['captcha', 'email', 'username']
        fields = ('password', 'tel')
        error_messages = {
            'username': {
                'required': "用户名不能为空",
            },
        }
        widgets = {
            'tel': forms.TextInput(attrs={
                'class': 'inputs',
                'placeholder': '手机号/用户名',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'inputs',
                'placeholder': '登录密码'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        tel = cleaned_data.get('tel', None)
        password = cleaned_data.get('password', None)
        if tel and password:
            res = User.objects.filter(tel=tel, password=password).first()
            if not res:
                raise ValidationError('用户名或密码有误！')