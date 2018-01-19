# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime
from WangEditor.models import WangEditorField

from django.db import models        # 导入models对象
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构",on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = WangEditorField(verbose_name='课程详情', default='')
    is_banner =models.BooleanField(default=False, verbose_name="是否轮播图")
    teacher = models.ForeignKey(Teacher, verbose_name="讲师",on_delete=models.CASCADE)
    degree = models.CharField(verbose_name='课程级别', choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=3)
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='课程封面图', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(verbose_name='课程类别', max_length=20, default='后端开发')
    tag = models.CharField(verbose_name='课程标签', max_length=10, default='')

    Uneed_know = models.CharField(max_length=300,verbose_name="课程须知", default="")
    teacher_tell = models.CharField(max_length=300, verbose_name="老师告诉你", default="")

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()

    def get_learn_users(self):              # 取该课程学习用户
        return self.usercourse_set.all()[:5]

    def get_chapter_nums(self):             # 获取章节数
        return self.lesson_set.all().count()
    get_chapter_nums.short_description = "章节数"              # 函数显示名称自定义

    def __unicode__(self):
        return self.name        # 设置在xadmin后台显示字段, 注意如果此表被另外的了外键关联了，这个返回字段就是外键表的外键名称


class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True                # 只为在admin中注册不同数据


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='外键课程',on_delete=models.CASCADE)      # 外键链表，外键连接Course表的主键，一对多关系
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加日期')

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name        # 设置在xadmin后台显示字段, 注意如果此表被另外的了外键关联了，这个返回字段就是外键表的外键名称

    def get_lesson_video(self):
        # 获取章节视频
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='外键章节',on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='视频名')
    url = models.CharField(max_length=200, default="", verbose_name='访问地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加日期')

    class Meta:
        verbose_name = '课程视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name        # 设置在xadmin后台显示字段, 注意如果此表被另外的了外键关联了，这个返回字段就是外键表的外键名称


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='外键课程',on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='课程资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加日期')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
