# -*- coding:utf8 -*-

from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentsView, VideoPlayView, \
    CourseQuestionView, CourseTestView, AddQuestionsView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    # 课程章节页
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    # 课程评论页
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    # 课程提问页
    url(r'^question/(?P<course_id>\d+)/$', CourseQuestionView.as_view(), name='course_question'),
    # 课程小测试页
    url(r'^test/(?P<video_id>\d+)/$', CourseTestView.as_view(), name='course_test'),
    # 添加课程评论页
    url(r'^add_comment/$', AddCommentsView.as_view(), name='add_acomment'),
    # 添加课程提问页
    url(r'^add_question/$', AddQuestionsView.as_view(), name='add_aquestion'),
    # 添加课程视频页
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),

]