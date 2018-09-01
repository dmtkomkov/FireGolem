from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import F
from datetime import date

from api.models import Payment, Category
from helpers.pagination import get_page


class MoneyView(LoginRequiredMixin, View):
    def get(self, request):
        all_dates = Payment.objects.values('spent').annotate(day_sum=Sum('amount')).order_by("-spent")
        categories = Category.objects.all().order_by("id")
        active_page = request.GET.get('page')

        dates, page_conf = get_page(all_dates, active_page)
        for pdate in dates:
            pdate['payments'] = Payment.objects.all().filter(spent=pdate['spent'])
            if pdate['day_sum'] <= 100:
                pdate['color'] = 'info'
            elif pdate['day_sum'] <= 200:
                pdate['color'] = 'warning'
            else:
                pdate['color'] = 'danger'

        page = {'dates': dates, 'categories': categories, 'today': date.today().isoformat()}
        page.update(page_conf)

        return render(request, 'money/home.html', page)

    def post(self, request):
        date_string = request.POST['date']
        amount = request.POST['amount']
        spent = date(*map(int, date_string.split('-')))
        oCategory = Category.objects.get(name=request.POST['category'])
        oPayment = Payment(amount=amount, spent=spent, category=oCategory)
        oPayment.save()
        return self.get(request)

    def delete(self, request):
        payment_id = request.DELETE["payment_id"]
        payment = Payment.objects.get(id=payment_id)
        payment.delete()
        return self.get(request)

class MoneyViewReport(LoginRequiredMixin, View):
    def get(self, request):
        all_months = Payment.objects.values(
            year=ExtractYear("spent"),
            month=ExtractMonth("spent"),
        ).exclude(year__isnull=True).annotate(
            day_sum=Sum("amount")
        ).order_by("-year", "-month")
        categories = Category.objects.all().order_by("id")
        active_page = request.GET.get('page')

        months, page_conf = get_page(all_months, active_page)
        for month in months:
            month["payments"] = Payment.objects.values(
                category_name = F("category__name"),
            ).filter(
                spent__month=month["month"],
                spent__year=month["year"]
            ).annotate(category_sum=Sum("amount")).all().order_by("category")
            print month

        page = {"months": months, "categories": categories}
        page.update(page_conf)

        return render(request, "money/report.html", page)

class MoneyViewGraph(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'money/graph.html')
