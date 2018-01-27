# -*- coding:utf8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse, CourseQuestions, CourseQuestions_Answers, \
    VideoTest
from utils.mixin_utils import LoginRequireMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")   # 所有数据传入  并且以 添加时间排序

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程搜索 --- 搜索栏
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)
                                             |Q(desc__icontains=search_keywords)
                                             |Q(detail__icontains=search_keywords))              # i 不区分大小写

        # 分类筛选, 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页   分页要放最后
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            'sort': sort,
            'hot_courses': hot_courses
        })

class CourseTestView(View):
    # 视频播放页面
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)  # 用户是否与该课程有关联，若没有则建立关系
            user_course.save()

        user_cousers = UserCourse.objects.filter(course=course)  #
        user_ids = [user_couser.user.id for user_couser in user_cousers]  # 提取所有user id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 用user id 提取这些user 所学过的课程
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        # 获取 学过该课程的用户还学过其他的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")

        all_resources = CourseResource.objects.filter(course=course)
        video_test = VideoTest.objects.filter(video_id=video_id)

        return render(request, "course-test.html", {
            "course": course,
            "course_recourses": all_resources,
            "relate_courses": relate_courses,
            "video": video,
            "video_test":video_test,
        })

class CourseTestUploadView(View):
    # 视频播放页面
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)  # 用户是否与该课程有关联，若没有则建立关系
            user_course.save()

        user_cousers = UserCourse.objects.filter(course=course)  #
        user_ids = [user_couser.user.id for user_couser in user_cousers]  # 提取所有user id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 用user id 提取这些user 所学过的课程
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        # 获取 学过该课程的用户还学过其他的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")

        all_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-test-upload.html", {
            "course": course,
            "course_recourses": all_resources,
            "relate_courses": relate_courses,
            "video": video,
        })

class VideoPlayView(View):
    # 视频播放页面
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)  # 用户是否与该课程有关联，若没有则建立关系
            user_course.save()

        user_cousers = UserCourse.objects.filter(course=course)  #
        user_ids = [user_couser.user.id for user_couser in user_cousers]  # 提取所有user id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 用user id 提取这些user 所学过的课程
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        # 获取 学过该课程的用户还学过其他的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")

        all_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "course_recourses": all_resources,
            "relate_courses": relate_courses,
            "video": video,
        })


class CourseDetailView(View):
    # 课程详情页
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_nums +=1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, "course-detail.html",{
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


class CourseInfoView(LoginRequireMixin, View):  #  通过权限认证
    # 课程章节信息
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        course.students +=1
        course.save()
        #查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)      # 用户是否与该课程有关联，若没有则建立关系
            user_course.save()

        user_cousers = UserCourse.objects.filter(course=course)             #
        user_ids = [user_couser.user.id for user_couser in user_cousers]    # 提取所有user id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 用user id 提取这些user 所学过的课程
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        # 获取 学过该课程的用户还学过其他的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")

        all_resources = CourseResource.objects.filter(course=course)

        return  render(request, "course-video.html", {
            "course": course,
            "course_recourses": all_resources,
            "relate_courses": relate_courses,
        })


class CourseCommentView(LoginRequireMixin, View):
    #  课程评论
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return  render(request, "course-comment.html", {
            "course": course,
            "course_recourses": all_resources,
            "all_comments": all_comments,
        })

class CourseQuestionView(LoginRequireMixin, View):
    #  课程提问
    def get(self, reuqest, course_id):
        course = Course.objects.get(id=int(course_id))

        all_resources = CourseResource.objects.filter(course=course)
        all_questions = CourseQuestions.objects.all()
        all_answers = CourseQuestions_Answers.objects.filter(course=course)
        return render(reuqest, "course-question.html", {
            "course": course,
            "course_recourses": all_resources,
            "all_questions": all_questions,
            "all_answers": all_answers,
        })


class AddCommentsView(View):
    # 用户添加课程评论
    def post(self, request):
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')

class AddQuestionsView(View):
    # 用户添加课程评论
    def post(self, request):
        course_id = request.POST.get("course_id", 0)
        questions = request.POST.get("questions", "")

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        if int(course_id) > 0 and questions:
            course_questions = CourseQuestions()
            course = Course.objects.get(id=int(course_id))
            course_questions.course = course
            course_questions.questions = questions
            course_questions.user = request.user
            course_questions.save()
            return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')

class AddAnswersView(View):
    # 用户添加课程评论
    def post(self, request):
        course_id = request.POST.get("course_id", 0)
        answers = request.POST.get("answers", "")
        question_id = request.POST.get("question_id", 0)

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        if int(course_id) > 0 and answers:
            course_questions_answers = CourseQuestions_Answers()
            course = Course.objects.get(id=int(course_id))
            course_questions_answers.course = course
            course_questions_answers.question = CourseQuestions.objects.get(id=int(question_id))
            course_questions_answers.answers = answers
            course_questions_answers.user = request.user
            course_questions_answers.save()
            return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')

class AddTestQuestionView(View):
    # 用户添加课程评论
    def post(self, request, video_id):
        question = request.POST.get("question", "")
        ansA = request.POST.get("ansA", "")
        ansB = request.POST.get("ansB", "")
        ansC = request.POST.get("ansC", "")
        ansD = request.POST.get("ansD", "")
        correctAns = request.POST.get("correctAns", "")

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        if int(video_id) > 0:
            videoTest = VideoTest()
            videoTest.video = Video.objects.get(id=int(video_id))
            videoTest.question = question
            videoTest.ansA = ansA
            videoTest.ansB = ansB
            videoTest.ansC = ansC
            videoTest.ansD = ansD
            videoTest.correctAns = correctAns
            videoTest.save()
            return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')
