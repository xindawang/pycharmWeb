# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect            # 导入django向浏览器返回方法
from django.core.urlresolvers import NoReverseMatch, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q                    # 并集 作用户登录方式 或判断
from django.views.generic.base import View        # 使用类重新定义函数
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm        # 导入登录页面表单认证
from .forms import UploadImageForm, UserInfoForm        # 上传头像Form
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequireMixin     # 需要登录权限
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from .models import Banner


class CustomBackend(ModelBackend):                      # 登录方式：邮箱 & 账号登录
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user =  UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html", {})
        return render(request, "login.html", {})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):  # 判断邮箱是否已经存在
                return render(request, "register.html", {'register_form': register_form, 'msg': '用户已经注册'})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册资源共享网"
            user_message.save()

            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html",{"register_form":register_form})


class LoginView(View):              # 类   登录流程，判断
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        login_form = LoginForm(request.POST)        # 加form验证，防止被绕过前台被攻击，一层保护，还可以过滤无效的登录；不用每次登录都去寻找数据库，为数据库减负
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名错误或密码错误！"})
        else:
            return render(request, "login.html", {"login_form":login_form})


class LogoutView(View):
    # 登出
    def get(self, request):
      logout(request)
      # Redirect to a success page.
      return HttpResponseRedirect(reverse("index"))


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email,'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    """密码找回的View"""
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {'email': email})  # 跳转到修改密码页面
        else:
            # active_fail.html在templates中新建的一个文件body中就一个<p>链接失效!</p>
            return render(request, "active_fail.html", {})
        return render(request, "login.html", {})


class ModifyPwdView(View):
    # 密码重置
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')

            if pwd1 != pwd2:
                return render(request, "password_reset.html", {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html", {})
        else:
            email = request.POST.get('email', '')
            return render(request, "password_reset.html", {'email': email, 'msg': modify_form})


class UserInfoView(LoginRequireMixin, View):    # 需要权限
    # 用户个人信息
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)          # instance作修改， 无instance就会新增
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequireMixin, View):   # 需要权限
    # 用户修改头像
    # def post(self, request):            # 技巧：在django admin/xadmin 对form定义为文件的时候自动对上传的文件做保存
                                # 利用这个特性， 用form的一个字段给他定义一个文件类型，把这个字段取出来，就是这个文件
                                # 再把它复制到user/image就是用户头像了
    #     image_form = UploadImageForm(request.POST, request.FILES)      # 实例化
    #     if image_form.is_valid():
    #         image = image_form.cleaned_data['image']
    #         request.user.image = image
    #         request.user.save()
    #         pass
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)      # 实例化
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class UpdatePwdView(LoginRequireMixin, View):
    # 在个人中心修改密码
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')

            if pwd1 != pwd2:
                return HttpResponse('{"status": "fail", "msg":"密码不一致"}', content_type='application/json')

            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequireMixin, View):
    # 发送修改邮箱-邮箱验证码
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')

        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequireMixin, View):
    # 修改个人邮箱-修改邮箱
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')         # 引入EmailVerify表

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email =email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequireMixin, View):
    # 我的课程
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)

        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses,
        })


class MyFavOrgView(LoginRequireMixin, View):
    # 我的收藏 课程机构
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)                # 遍历

        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list,
        })


class MyFavTeacherView(LoginRequireMixin, View):
    # 我的收藏 授课讲师
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)                # 遍历

        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list,
        })


class MyFavCourseView(LoginRequireMixin, View):
    # 我的收藏 公开课
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)                # 遍历

        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
        })


class MyMessageView(LoginRequireMixin, View):
    # 我的消息
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空未读消息
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对 我的消息 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 1, request=request)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            "messages": messages,
        })


class IndexView(View):
    # 资源共享网首页
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404    # 这个状态码会影响浏览器的显示
    return response