# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 06:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0008_auto_20170803_1525'),
        ('member', '0003_myuser_relations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.MyGroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='group',
            field=models.ManyToManyField(related_name='member', through='member.Membership', to='group.MyGroup'),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('user', 'group')]),
        ),
    ]
