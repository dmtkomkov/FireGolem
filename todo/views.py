from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict

from api.models import Area, Project, Task, TaskStatus
from helpers.pagination import get_page

PPP = 10  # POSTS_PER_PAGE
PML = 11  # PAGINATOR_MAX_LENGTH
PHL = (PML - 1) // 2 # PAGINATOR_HALF_LENGTH


class ProjectView(LoginRequiredMixin, View):
    def get(self, request):
        all_projects = Project.objects.all()
        active_page = request.GET.get('page')

        projects, page_conf = get_page(all_projects, active_page)
        page = {'projects': projects}
        page.update(page_conf)

        return render(request, 'project/home.html', page)

    def post(self, request):
        name = request.POST.get('name')
        project = Project(name=name)
        project.save()
        return self.get(request)


class AreaView(LoginRequiredMixin, View):
    def get(self, request):
        all_areas = Area.objects.all()
        active_page = request.GET.get('page')

        areas, page_conf = get_page(all_areas, active_page)
        page = {'areas': areas}
        page.update(page_conf)

        return render(request, 'area/home.html', page)

    def post(self, request):
        name = request.POST.get('name')
        area = Area(name=name)
        area.save()
        return self.get(request)


class TodoView(LoginRequiredMixin, View):
    def get(self, request):
        all_todos = Task.objects.all().filter(deleted=False).order_by("updated")
        active_page = request.GET.get('page')

        todos, page_conf = get_page(all_todos, active_page)
        page = {'todos': todos}
        page.update(page_conf)

        return render(request, 'todo/home.html', page)

    def post(self, request):
        name = request.POST.get('name')
        task = Task(name=name)
        task.save()
        return self.get(request)


class TodoDetails(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        return render(request, 'todo/details.html',
                      {
                          'task': task,
                      })

    def put(self, request, task_id):
        """
        Process AJAX request for bootstrap-editable plugin
        """
        # TODO: error handling
        request.PUT = QueryDict(request.body)
        task = Task.objects.get(id=task_id)
        name = request.PUT.get("name")
        name = name.split("-")[1] # convert attribute value task-<name> to <name>
        value = request.PUT.get("value")
        if name == "status":
            value = TaskStatus.objects.get(id=int(value))
        setattr(task, name, value)
        task.save()
        return HttpResponse('')
