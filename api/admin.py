from django.contrib import admin

from api.models import Post, Payment, Category, UserIcon, WorkLog, Label, LabelGroup

for model in (Post, Payment, Category, UserIcon, WorkLog, Label, LabelGroup):
    admin.site.register(model)
