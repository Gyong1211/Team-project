# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20170728_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='profile_img',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
