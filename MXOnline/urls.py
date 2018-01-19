# -*- coding:utf8 -*-

"""MXOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve           # 处理静态文件

import xadmin               # 导入xadmin

from users.views import LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from users.views import IndexView
from MXOnline.settings import MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'logout/$', LogoutView.as_view(), name='logout'),

    url(r'^register/$', RegisterView.as_view(), name='register'),                    #注册
    url(r'^captcha/',include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),  # 忘记密码链接
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),  # 重置密码链接
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),  # 重置密码链接

    # 课程机构url配置                                     url分组
    url(r'^org/',include('organization.urls', namespace="org")),         # 命名空间，防止有两个相同 name 的冲突，
                                                                        # 既用了namespace就可以在不同url有相同的name

    # 课程相关url配置                                     url分组
    url(r'^course/',include('courses.urls', namespace="course")),

    # 用户个人信息相关url配置                             url分组
    url(r'^users/',include('users.urls', namespace="users")),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # 富文本url
    url(r'^Reditor/', include('WangEditor.urls')),
]
app_name = 'mxonline'
# 全局404页面配置
handler400 = "users.views.page_not_found"
handler500 = "users.views.page_error"


