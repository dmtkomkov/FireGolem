# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2021-02-21 16:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_related_name_group_labels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name=b'assignee',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
