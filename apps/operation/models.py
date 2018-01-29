# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models              # 导入models对象

from users.models import UserProfile      # 导入用户信息表
from courses.models import Course, Video  # 导入课程表


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course_name = models.CharField(max_length=50, verbose_name='课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户',on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程',on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='评论时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class CourseQuestions(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户',on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程',on_delete=models.CASCADE)
    questions = models.CharField(max_length=200, verbose_name='提问')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='提问时间')
    lesson_id = models.IntegerField(verbose_name='章节id')

    class Meta:
        verbose_name = '课程提问'
        verbose_name_plural = verbose_name

class CourseQuestions_Answers(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户',on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程',on_delete=models.CASCADE)
    question = models.ForeignKey(CourseQuestions, verbose_name='提问',on_delete=models.CASCADE)
    answers = models.CharField(max_length=200, verbose_name='回答')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='回答时间')

    class Meta:
        verbose_name = '课程回答'
        verbose_name_plural = verbose_name

class VideoTest(models.Model):
    video = models.ForeignKey(Video, verbose_name='视频',on_delete=models.CASCADE)
    question = models.CharField(max_length=200, verbose_name='题目')
    ansA = models.CharField(max_length=50, verbose_name='选项A')
    ansB = models.CharField(max_length=50, verbose_name='选项B')
    ansC = models.CharField(max_length=50, verbose_name='选项C')
    ansD = models.CharField(max_length=50, verbose_name='选项D')
    correctAns = models.CharField(max_length=12, verbose_name='正确答案')
    analysis = models.CharField(max_length=200, verbose_name='解析')

    class Meta:
        verbose_name = '课程小测试'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户',on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name='收藏数据ID')
    fav_type = models.IntegerField(choices=((1, '课程'), (2, '课程机构'), (3, '讲师')), default=1, verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='收藏时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name='接收用户id')    # 0表示所有用户
    message = models.CharField(max_length=500, verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='消息时间')
    lesson_id = models.IntegerField()
    course_id = models.IntegerField()

    class Meta:
        verbose_name = '用户消息表'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='学习用户',on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='学习课程',on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='学习时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name