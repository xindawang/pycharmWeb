# -*- coding:utf8 -*-
import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):               # 自定义数据表管理器类
    # 设置xadmin后台显示字段
    list_display = ['name', 'desc', 'add_time']
    # 设置xadmin后台搜索字段，注意：搜索字段如果有时间类型会报错
    search_fields = ['name', 'desc', 'detail']
    # 设置xadmin后台过滤器帅选字段，时间用过滤器来做
    list_filter = ['name', 'desc', 'add_time']
xadmin.site.register(CityDict, CityDictAdmin)     # 将数据表注册到xadmin后台显示


class CourseOrgAdmin(object):
    # 设置xadmin后台显示字段
    list_display = ['name', 'desc', 'click', 'fav_nums', 'image', 'address', 'add_time']
    # 设置xadmin后台搜索字段，注意：搜索字段如果有时间类型会报错
    search_fields = ['name', 'desc', 'click', 'fav_nums', 'image', 'address']
    # 设置xadmin后台过滤器帅选字段，时间用过滤器来做
    list_filter = ['name', 'desc', 'click', 'fav_nums', 'image', 'address', 'add_time']  # course__name 表示通过course外键字段查询关联表里的name字段
    relfield_style = 'fk-ajax'
xadmin.site.register(CourseOrg, CourseOrgAdmin)  # 将数据表注册到xadmin后台显示


class TeacherAdmin(object):
    # 设置xadmin后台显示字段
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click', 'fav_nums', 'add_time']
    # 设置xadmin后台搜索字段，注意：搜索字段如果有时间类型会报错
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click', 'fav_nums']
    # 设置xadmin后台过滤器帅选字段，时间用过滤器来做
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click', 'fav_nums', 'add_time']
xadmin.site.register(Teacher, TeacherAdmin)   # 将数据表注册到xadmin后台显示