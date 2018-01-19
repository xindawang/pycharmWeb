# -*- coding:utf8 -*-

from django.conf.urls import url, include

from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView
from .views import TeacherListView, TeacherDetialView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$',OrgView.as_view(),name='org_list'),

    url(r'^add_ask/$', AddUserAskView.as_view(),name='add_ask'),

    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),

    # 用户收藏
    url(r'^add_fav/$', AddFavView.as_view(),name='add_fav'),

    # 讲师页 相关url配置                                     url分组
    url(r'^teacher/list',TeacherListView.as_view(), name="teacher_list"),

    # 讲师详情页
    url(r'^teacher/detial/(?P<teacher_id>\d+)/$', TeacherDetialView.as_view(), name='teacher_detial'),

]