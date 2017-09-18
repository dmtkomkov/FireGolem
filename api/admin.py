from django.contrib import admin

from api.models import Post, Task, TaskStatus, WorkLog, Domain, Aria, Project

for model in (Post, Task, TaskStatus, WorkLog, Domain, Aria, Project):
    admin.site.register(model)