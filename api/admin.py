from django.contrib import admin

from api.models import Post, Task, TaskStatus, WorkLog, Area, Project

for model in (Post, Task, TaskStatus, WorkLog, Area, Project):
    admin.site.register(model)