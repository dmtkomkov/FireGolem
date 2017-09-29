from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from api.models import Task

PPP = 10  # POSTS_PER_PAGE
PML = 11  # PAGINATOR_MAX_LENGTH
PHL = (PML - 1) // 2 # PAGINATOR_HALF_LENGTH


class TodoView(LoginRequiredMixin, View):
    def get(self, request):
        all_todos = Task.objects.all().filter(deleted=False).order_by("updated")

        paginator = Paginator(all_todos, PPP)
        active_page = request.GET.get('page')

        try:
            active_page = int(active_page)
            todos = paginator.page(active_page)
        except (ValueError, TypeError, EmptyPage):  # get the last page in case of wrong active page
            active_page = paginator.num_pages
            todos = paginator.page(active_page)

        if paginator.num_pages <= PML:  # num_pages less than maximum
            page_numbers = range(1, paginator.num_pages + 1)
        elif active_page <= PHL:
            page_numbers = range(1, PML + 1)
        elif active_page >= paginator.num_pages - PHL:
            page_numbers = range(paginator.num_pages - PML + 1, paginator.num_pages + 1)
        else:
            page_numbers = range(active_page - PHL, active_page + PHL + 1)

        # next and prev button references on the pagination bar
        if active_page == 1:
            prev_page = None
        elif active_page <= PML:
            prev_page = 1
        else:
            prev_page = active_page - PML
        if active_page == paginator.num_pages:
            next_page = None
        elif active_page >= paginator.num_pages - PML:
            next_page = paginator.num_pages
        else:
            next_page = active_page + PML

        return render(request, 'todo/home.html',
                      {'todos': todos,
                       'active_page': active_page,
                       'page_numbers': page_numbers,
                       'prev_page': prev_page,
                       'next_page': next_page
                       })


class TodoDetails(LoginRequiredMixin, View):
    def get(self, request, task_id):
        return render(request, 'todo/details.html',
                      {
                          'task_id': task_id,
                      })
