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


class ProjectDetails(LoginRequiredMixin, View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        return render(request, 'project/details.html', { 'project': project })

    def put(self, request, project_id):
        request.PUT = QueryDict(request.body)
        project = Project.objects.get(id=project_id)
        name = request.PUT.get("name")
        name = name.split("-")[1]                                 # convert attribute value task-<name> to <name>
        value = request.PUT.get("value")
        setattr(project, name, value)                             # Change model attribute
        project.save()
        return HttpResponse('')


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


class AreaDetails(LoginRequiredMixin, View):
    def get(self, request, area_id):
        area = Area.objects.get(id=area_id)
        return render(request, 'area/details.html', { 'area': area })

    def put(self, request, area_id):
        request.PUT = QueryDict(request.body)
        area = Area.objects.get(id=area_id)
        name = request.PUT.get("name")
        name = name.split("-")[1]                                 # convert attribute value task-<name> to <name>
        value = request.PUT.get("value")
        setattr(area, name, value)                                # Change model attribute
        area.save()
        return HttpResponse('')


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
        statuses = TaskStatus.objects.all()
        statuses_source = [{'value': int(s.id), 'text': str(s.status)} for s in statuses]
        areas = Area.objects.all().filter(deleted=False)
        areas_source = [{'value': int(a.id), 'text': str(a.name)} for a in areas]
        projects = Project.objects.all().filter(deleted=False)
        projects_source = [{'value': int(p.id), 'text': str(p.name)} for p in projects]
        return render(request, 'todo/details.html',
                      {
                          'task': task,
                          'statuses_source': str(statuses_source),
                          'areas_source': str(areas_source),
                          'projects_source': str(projects_source),
                      })

    def put(self, request, task_id):
        """
        Process AJAX request for bootstrap-editable plugin
        """
        # TODO: error handling
        # TODO: Empty choice for project and area
        # TODO: update "Updated Date" on put
        request.PUT = QueryDict(request.body)
        task = Task.objects.get(id=task_id)
        name = request.PUT.get("name")
        name = name.split("-")[1]                                 # convert attribute value task-<name> to <name>
        value = request.PUT.get("value")
        model = {"status": TaskStatus, "area": Area, "project": Project}[name]      # Get model by attribute name
        value = model.objects.get(id=int(value))
        setattr(task, name, value)                                # Change model attribute
        task.save()
        return HttpResponse('')
