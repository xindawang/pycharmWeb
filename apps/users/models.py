# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models        # 导入models对象
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):       # 创建类必须继承models.Model，类名将是在数据库里的表名称
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(max_length=10, verbose_name='性别', choices=(("male", "男"), ("female", "女")), default='male')
    address = models.CharField(max_length=100, verbose_name='地区', null=True, blank=True)
    mobile = models.CharField(max_length=11, verbose_name='手机', null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', verbose_name='头像', default='image/default.png', max_length=100)
    is_teacher = models.BooleanField(default=False)
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username        # 设置在xadmin后台显示字段, 注意如果此表被另外的了外键关联了，这个返回字段就是外键表的外键名称

    def unread_nums(self):
        # 获取用户未读消息数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=12, choices=(('register', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')), verbose_name='邮箱验证类型')
    send_time = models.DateTimeField(verbose_name='生成时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)

class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图', max_length=100)  # 图片路径banner/%Y/%m  /年/月
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='轮播图顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='轮播图添加时间')

    class Meta:
        verbose_name = '网站轮播图'
        verbose_name_plural = verbose_name