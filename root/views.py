from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from api.models import Post, Task, Payment
from django.db.models import Sum
from datetime import datetime, timedelta, date


class RootView(LoginRequiredMixin, View):
    def get(self, request):
        blogStats = {}  # Build data for blog dashboard

        blogStats['count'] = Post.objects.count()

        if blogStats['count'] > 0:
            latestPost = Post.objects.order_by('-created')[0]
            daysDelta = (datetime.today() - latestPost.created).days
            if not daysDelta:
                blogStats['latest'] = "today"
            else:
                blogStats['latest'] = "{} days ago".format(daysDelta)
        else:
            blogStats['latest'] = "No posts"

        moneyStats = {}  # Build data for money dashboard

        todayPayments = Payment.objects.filter(spent=date.today()).aggregate(Sum('amount'))['amount__sum'] or 0
        moneyStats['today'] = todayPayments

        monthPayments = Payment.objects.filter(spent__month=date.today().month, spent__year=date.today().year).aggregate(Sum('amount'))['amount__sum'] or 0
        moneyStats['month'] = monthPayments

        return render(request, 'root/home.html', {
            'blogStats': blogStats,
            'moneyStats': moneyStats,
        })
