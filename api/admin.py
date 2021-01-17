from django.contrib import admin

from api.models import Post, Task, Payment, Category, UserIcon, WorkLog, Label, LabelGroup

for model in (Post, Task, Payment, Category, UserIcon, WorkLog, Label, LabelGroup):
    admin.site.register(model)
