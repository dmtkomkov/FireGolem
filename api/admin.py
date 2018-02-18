from django.contrib import admin

from api.models import Post, Task, TaskStatus, WorkLog, Area, Project, Payment, Category, UserIcon

for model in (Post, Task, TaskStatus, WorkLog, Area, Project, Payment, Category, UserIcon):
    admin.site.register(model)
