from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from api.models import Task


class TodoView(LoginRequiredMixin, View):
    def get(self, request):
        todos = Task.objects.all().filter(deleted=False).order_by("updated")
        return render(request, 'todo/home.html',
                      {
                          'todos': todos,
                      })


class TodoDetails(LoginRequiredMixin, View):
    def get(self, request, task_id):
        return render(request, 'todo/details.html',
                      {
                          'task_id': task_id,
                      })
