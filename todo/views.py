from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from api.models import Area, Project, Task, TaskStatus, Post, WorkLog
from helpers.pagination import get_page
from helpers.task import get_estimations

from datetime import datetime


class ProjectView(LoginRequiredMixin, View):
    def get(self, request):
        all_projects = Project.objects.all().order_by("name")
        active_page = request.GET.get('page')

        projects, page_conf = get_page(all_projects, active_page)
        page = {'projects': projects, 'title': 'Projects'}
        page.update(page_conf)

        return render(request, 'project/home.html', page)

    def post(self, request):
        name = request.POST.get('name')
        project = Project(name=name)
        project.save()
        return self.get(request)


class ProjectDetails(LoginRequiredMixin, View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        return render(request, 'project/details.html', {'project': project, 'title': 'Project Details'})

    def put(self, request, project_id):
        request.PUT = QueryDict(request.body)
        project = Project.objects.get(id=project_id)
        name = request.PUT.get("name")
        name = name.split("-")[1]                                 # convert attribute value task-<name> to <name>
        value = request.PUT.get("value")
        setattr(project, name, value)                             # Change model attribute
        project.save()
        return HttpResponse('')

    def delete(self, request, project_id):
        project = Project.objects.get(id=project_id)
        project.delete()
        return redirect(reverse('project:home'))


class AreaView(LoginRequiredMixin, View):
    def get(self, request):
        all_areas = Area.objects.all().order_by("name")
        active_page = request.GET.get('page')

        areas, page_conf = get_page(all_areas, active_page)
        page = {'areas': areas, 'title': 'Areas'}
        page.update(page_conf)

        return render(request, 'area/home.html', page)

    def post(self, request):
        name = request.POST.get('name')
        area = Area(name=name)
        area.save()
        return self.get(request)


class AreaDetails(LoginRequiredMixin, View):
    def get(self, request, area_id):
        area = Area.objects.get(id=area_id)
        return render(request, 'area/details.html', {'area': area, 'title': 'Area Details'})

    def put(self, request, area_id):
        request.PUT = QueryDict(request.body)
        area = Area.objects.get(id=area_id)
        name = request.PUT.get("name")
        name = name.split("-")[1]                                 # convert attribute value task-<name> to <name>
        value = request.PUT.get("value")
        setattr(area, name, value)                                # Change model attribute
        area.save()
        return HttpResponse('')

    def delete(self, request, area_id):
        area = Area.objects.get(id=area_id)
        area.delete()
        return redirect(reverse('area:home'))


class TodoView(LoginRequiredMixin, View):
    def get(self, request):
        all_statuses = TaskStatus.objects.all().order_by("id")
        all_areas = Area.objects.all().order_by("name")
        all_projects = Project.objects.all().order_by("name")
        all_todos = Task.objects.all().filter(deleted=False).order_by("-updated")

        status_id = request.GET.get("status")
        area_id = request.GET.get("area")
        project_id = request.GET.get("project")

        if status_id:
            all_todos = all_todos.filter(status=status_id)
        else:
            all_todos = all_todos.exclude(status__in=(21, 22))  # Exclude cancelled and closed tasks

        if area_id:
            all_todos = all_todos.filter(area=area_id)
        if project_id:
            all_todos = all_todos.filter(project=project_id)

        active_page = request.GET.get('page')

        todos, page_conf = get_page(all_todos, active_page)
        page = {
            'statuses': all_statuses,
            'areas': all_areas,
            'projects': all_projects,
            'todos': todos,
            'title': 'Tasks',
        }
        page.update(page_conf)

        return render(request, 'todo/home.html', page)

    def post(self, request):
        name = request.POST.get('name')
        task = Task(name=name)

        status_id = request.GET.get("status")
        area_id = request.GET.get("area")
        project_id = request.GET.get("project")

        if status_id:
            task.status = TaskStatus.objects.get(id=status_id)
        if area_id:
            task.area = Area.objects.get(id=area_id)
        if project_id:
            task.project = Project.objects.get(id=project_id)

        task.save()
        return self.get(request)


class TodoDetails(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        statuses = TaskStatus.objects.all().order_by("id")
        statuses_source = [{'value': int(s.id), 'text': str(s.status)} for s in statuses]
        fake_source = [{'value': 'null', 'text': 'Empty'}]              # Fake value represents database null
        areas = Area.objects.all().order_by("id").order_by("name")
        areas_source = fake_source + [{'value': int(a.id), 'text': str(a.name)} for a in areas]
        projects = Project.objects.all().order_by("id").order_by("name")
        projects_source = fake_source + [{'value': int(p.id), 'text': str(p.name)} for p in projects]
        estimations_source = get_estimations()
        posts = Post.objects.filter(worklog__task = task_id).order_by("-created")
        return render(request, 'todo/details.html',
                      {
                          'task': task,
                          'posts': posts,
                          'title': 'Task Details',
                          'statuses_source': str(statuses_source),
                          'areas_source': str(areas_source),
                          'projects_source': str(projects_source),
                          'estimations_source': str(estimations_source),
                      })

    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)                              # Get Task
        log = request.POST.get("worklog")
        comment = request.POST.get("comment")
        title = " ".join(["[WorkLog {0}]".format(log), task.name])
        post = Post(title=title, body=comment)                           # Create Post
        post.user = request.user
        post.save()
        worklog = WorkLog(task=task, log=log, post=post)              # Create WorkLog
        worklog.save()
        task.updated = datetime.now()
        task.save()
        return self.get(request, task_id)


    def put(self, request, task_id):
        """
        Process AJAX request for bootstrap-editable plugin
        """
        request.PUT = QueryDict(request.body)
        task = Task.objects.get(id=task_id)
        name = request.PUT.get("name")
        name = name.split("-")[1]                                 # convert attribute value task-<name> to <name>
        value = request.PUT.get("value")
        if name in ("status", "area", "project"):                 # Get model to assign
            model = {                                             # Get model by attribute name
                "status": TaskStatus,
                "area": Area,
                "project": Project
            }[name]
            if value == 'null':
                value = None                                      # Process special case when attribute is null
            else:
                value = model.objects.get(id=int(value))          # Get db object by id
        setattr(task, name, value)                                # Change model attribute
        task.updated = datetime.now()                             # Change updated date
        task.save()
        return HttpResponse('')

    def delete(self, request, task_id):
        task = Task.objects.get(id=task_id)
        task.deleted = True
        task.save()
        return redirect(reverse('todo:home'))
