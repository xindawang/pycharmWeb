# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models        # 导入models对象


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市')
    desc = models.CharField(max_length=200, verbose_name='描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加日期')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name        # 设置在xadmin后台显示字段, 注意如果此表被另外的了外键关联了，这个返回字段就是外键表的外键名称


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='机构描述')
    tag = models.CharField(default="全国知名", max_length=10, verbose_name='机构标签')
    category = models.CharField(default="pxjg", verbose_name="机构类别", max_length=20, choices=(("pxjg", "培训机构"),("gx", "高校"),("gr", "个人")))
    click = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='封面图', max_length=100)
    address = models.CharField(max_length=150, verbose_name='机构地址')
    city = models.ForeignKey(CityDict, verbose_name='外键城市表',on_delete=models.CASCADE,)
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加日期')

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    # 获取机构课程老师数量
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name        # 设置在xadmin后台显示字段, 注意如果此表被另外的了外键关联了，这个返回字段就是外键表的外键名称

class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name='外键所属机构',on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='教师名')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    age = models.IntegerField(default=18, verbose_name='年龄')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='头像', max_length=100, default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加日期')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name  # 设置在xadmin后台显示字段, 注意如果此表被另外的了外键关联了，这个返回字段就是外键表的外键名称

    def get_course_nums(self):
        return self.course_set.all().count()
