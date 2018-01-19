# -*- coding:utf8 -*-
import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrg


class LessonInline(object):         # 联合调用2张表 ，方便添加课程章节
    model = Lesson
    extra = 0

class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):               # 自定义数据表管理器类
    # 设置xadmin后台显示字段
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'get_chapter_nums',
                    'fav_nums', 'image', 'click_nums', 'add_time']         # 'get_chapter_nums', 函数调用
    # 设置xadmin后台搜索字段，注意：搜索字段如果有时间类型会报错
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                     'fav_nums', 'image', 'click_nums']
    # 设置xadmin后台过滤器帅选字段，时间用过滤器来做
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                   'fav_nums', 'image', 'click_nums', 'add_time']
    ordering = ['-click_nums']                              # 列表默认排序显示
    # readonly_fields = ['click_nums', 'fav_nums']            # 可读不可写
    exclude = ['click_nums', 'fav_nums']                    # 不可读即不可写
    inlines = [LessonInline, CourseResourceInline]                    # 联合 调2个表，方便添加课程章节
    list_editable = ['degree', 'desc']              # 现场可编辑
    style_fields = {'detail': 'WangEditor'}
    import_excel = True



    def queryset(self):                             # 同一张表 两个管理器
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs


    def save_models(self):          # 在保存课程后，统计机构课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    # def post(self, request, *args, **kwargs):       # excel 重载函数 读取excel表内容
    #     if 'excel' in request.FILES:
    #         pass        # 后可以加人和函数
    #     return super(CourseAdmin, self).post(request, args, kwargs)

xadmin.site.register(Course, CourseAdmin)     # 将数据表注册到xadmin后台显示


class BannerCourseAdmin(object):               # 自定义数据表管理器类
    # 设置xadmin后台显示字段
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                    'fav_nums', 'image', 'click_nums', 'add_time']
    # 设置xadmin后台搜索字段，注意：搜索字段如果有时间类型会报错
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                     'fav_nums', 'image', 'click_nums']
    # 设置xadmin后台过滤器帅选字段，时间用过滤器来做
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                   'fav_nums', 'image', 'click_nums', 'add_time']
    ordering = ['-click_nums']                              # 列表默认排序显示
    # readonly_fields = ['click_nums', 'fav_nums']            # 可读不可写
    exclude = ['click_nums', 'fav_nums']                    # 不可读即不可写
    inlines = [LessonInline, CourseResourceInline]                    # 联合 调2个表，方便添加课程章节


    def queryset(self):                                 # 同一张表 两个管理器
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

xadmin.site.register(BannerCourse, BannerCourseAdmin)     # 将数据表注册到xadmin后台显示


class LessonAdmin(object):
    # 设置xadmin后台显示字段
    list_display = ['course', 'name', 'add_time']
    # 设置xadmin后台搜索字段，注意：搜索字段如果有时间类型会报错
    search_fields = ['name']
    # 设置xadmin后台过滤器帅选字段，时间用过滤器来做
    list_filter = ['course__name', 'name', 'add_time']      # course__name 表示通过course外键字段查询关联表里的name字段
xadmin.site.register(Lesson, LessonAdmin)   # 将数据表注册到xadmin后台显示


class VideoAdmin(object):
    # 设置xadmin后台显示字段
    list_display = ['lesson', 'name', 'add_time']
    # 设置xadmin后台搜索字段，注意：搜索字段如果有时间类型会报错
    search_fields = ['lesson', 'name']
    # 设置xadmin后台过滤器帅选字段，时间用过滤器来做
    list_filter = ['lesson', 'name', 'add_time']      # lesson__name 表示通过lesson外键字段查询关联表里的name字段
xadmin.site.register(Video, VideoAdmin)   # 将数据表注册到xadmin后台显示


class CourseResourceAdmin(object):
    # 设置xadmin后台显示字段
    list_display = ['course', 'name', 'download','add_time']
    # 设置xadmin后台搜索字段，注意：搜索字段如果有时间类型会报错
    search_fields = ['course', 'name', 'download']
    # 设置xadmin后台过滤器帅选字段，时间用过滤器来做
    list_filter = ['course', 'name', 'download','add_time']      # lesson__name 表示通过lesson外键字段查询关联表里的name字段
xadmin.site.register(CourseResource, CourseResourceAdmin)   # 将数据表注册到xadmin后台显示