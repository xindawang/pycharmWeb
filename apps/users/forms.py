# -*- coding:utf-8 -*-

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile

class LoginForm(forms.Form):                                    # 表单验证 登录
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):                                  # 表单验证 注册
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"})


class ForgetForm(forms.Form):                                   # 表单验证 忘记密码
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ModifyPwdForm(forms.Form):                                # 表单验证 重置密码
    password1 = forms.CharField(required=True, min_length=8)  # 最小长度8
    password2 = forms.CharField(required=True, min_length=8)  # 最小长度8


class UploadImageForm(forms.ModelForm):   # ModelForm
    class Meta:                      # 取出Model
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):   # ModelForm
    class Meta:                      # 取出Model
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']