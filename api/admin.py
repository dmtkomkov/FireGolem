from django.contrib import admin

from api.models import Post, Task, TaskStatus, WorkLog, Area, Project, Payment, Category

for model in (Post, Task, TaskStatus, WorkLog, Area, Project, Payment, Category):
    admin.site.register(model)
