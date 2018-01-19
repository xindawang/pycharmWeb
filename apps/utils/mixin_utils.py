# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequireMixin(object):                        # 检测是否登录， 权限

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequireMixin, self).dispatch(request, *args, **kwargs)