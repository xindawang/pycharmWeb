# -*- coding: utf-8 -*-

from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MXOnline.settings import  EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkIiMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""  # 记录邮件标题
    email_body = ""  # 记录邮件内容

    if send_type == "register":
        email_title = "慕学在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 发送邮件
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = '密码重置链接'
        email_body = '请点击链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 发送邮件

        if send_status:
            pass

    elif send_type == 'update_email':
        email_title = '邮箱修改-验证码'
        email_body = '请点击链接重置你的密码：{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 发送邮件

        if send_status:
            pass


