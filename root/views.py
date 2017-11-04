from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class RootView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'root/home.html', {'title': 'Dashboard'})
