# -*- coding:utf8 -*-

import xadmin
from xadmin import views

from. models import EmailVerifyRecord, Banner


class GlobalSetting(object):
    site_title = "后台管理系统"
    site_footer = "资源共享网站"
    menu_style = 'accordion'  # 'accordion'
xadmin.site.register(views.CommAdminView, GlobalSetting)


class EmailVerifyRecordAdmin(object):
    # 设置xadmin后台显示字段
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 设置xadmin后台搜索字段，注意：搜索字段如果有时间类型会报错
    search_fields = ['code', 'email', 'send_type']
    # 设置xadmin后台过滤器帅选字段，时间用过滤器来做
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-book'
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class BannerAdmin(object):
    # 设置xadmin后台显示字段
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    # 设置xadmin后台搜索字段，注意：搜索字段如果有时间类型会报错
    search_fields = ['title', 'image', 'url', 'index']
    # 设置xadmin后台过滤器帅选字段，时间用过滤器来做
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
xadmin.site.register(Banner, BannerAdmin)  # 将数据表注册到xadmin后台显示




