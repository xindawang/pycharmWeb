# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-23 22:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_courseorg_cateory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseorg',
            old_name='cateory',
            new_name='category',
        ),
    ]
