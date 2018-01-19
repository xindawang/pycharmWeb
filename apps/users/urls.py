# -*- coding:utf8 -*-

from django.conf.urls import url, include

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView
from .views import MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    # 个人中心 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),

    # 个人中心 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),

    # 个人中心 用户密码修改
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 个人中心 修改邮箱-邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),

    # 个人中心 修改邮箱-修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 个人中心 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),

    # 个人中心 我的收藏 课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),

    # 个人中心 我的收藏 授课讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),

    # 个人中心 我的收藏 公开课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),

    # 个人中心 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
]