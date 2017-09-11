from django.contrib import admin

from api.models import Post, Task, TaskStatus, WorkLog

for model in (Post, Task, TaskStatus, WorkLog):
    admin.site.register(model)