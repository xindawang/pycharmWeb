# -*- coding:utf-8 -*-

import re           # python基础
from django import forms

from operation.models import UserAsk

class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):                                         # 对mobile 自定义验证        其他字段由Model定义的 作验证
        # 验证手机号码合法
        mobile = self.cleaned_data['mobile']
        REGEX_MOBIE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBIE)
        if p.match(mobile):
            return mobile
        else:
            return forms.ValidationError("手机号码非法", code="mobile_invald")
