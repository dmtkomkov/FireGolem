from django.contrib import admin

from api.models import Post, Task, TaskStatus, WorkLog, Aria, Project

for model in (Post, Task, TaskStatus, WorkLog, Aria, Project):
    admin.site.register(model)