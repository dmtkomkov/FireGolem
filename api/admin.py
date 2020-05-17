from django.contrib import admin

from api.models import Post, Task, Payment, Category, UserIcon

for model in (Post, Task, Payment, Category, UserIcon):
    admin.site.register(model)
