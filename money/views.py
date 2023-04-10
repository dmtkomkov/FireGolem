from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import F, Case, When

import calendar
from datetime import date
from api.models import Payment, Category
from helpers.pagination import get_page


class MoneyView(LoginRequiredMixin, View):
    def get(self, request):
        all_dates = Payment.objects.values('spent'  ).annotate(
            total_pln=Sum(Case(When(currency='PLN', then='amount'), default=0)),
            total_eur=Sum(Case(When(currency='EUR', then='amount'), default=0)),
        ).order_by("-spent")
        categories = Category.objects.all().order_by("id")
        active_page = request.GET.get('page')

        dates, page_conf = get_page(all_dates, active_page)
        for pdate in dates:
            pdate['payments'] = Payment.objects.all().filter(spent=pdate['spent'])

        page = {'dates': dates, 'categories': categories, 'today': date.today().isoformat()}
        page.update(page_conf)

        return render(request, 'money/home.html', page)

    def post(self, request):
        date_string = request.POST['date']
        amount = request.POST['amount']
        currency = request.POST['currency']
        spent = date(*map(int, date_string.split('-')))
        oCategory = Category.objects.get(name=request.POST['category'])
        oPayment = Payment(amount=amount, currency=currency, spent=spent, category=oCategory)
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
            month_total_pln=Sum(Case(When(currency='PLN', then='amount'), default=0)),
            month_total_eur=Sum(Case(When(currency='EUR', then='amount'), default=0)),
        ).order_by("-year", "-month")
        categories = Category.objects.all().order_by("id")
        active_page = request.GET.get("page")

        months, page_conf = get_page(all_months, active_page)
        for month in months:
            # Get payment details from database
            # [{'name': 'food', 'sum': 4}, {'name': 'hobby', 'sum': 7}]
            payment_details = Payment.objects.values(
                name = F("category__name"),
            ).filter(
                spent__month=month["month"],
                spent__year=month["year"]
            ).annotate(
                month_category_total_pln=Sum(Case(When(currency='PLN', then='amount'), default=0)),
                month_category_total_eur=Sum(Case(When(currency='EUR', then='amount'), default=0)),
            ).all().order_by("category")
            # Convert payment details to convenient format
            # {'food': 4, 'hobby': 7}
            payment_details = dict((p["name"], {'pln': p["month_category_total_pln"], 'eur': p["month_category_total_eur"]}) for p in payment_details)
            # Create table row
            month['payments'] = [payment_details.get(c.name, {'pln': 0, 'eur': 0}) for c in categories]
            # Convert month and year to represent in template
            month['month'] = calendar.month_name[month['month']][:3]
            month['year'] = month['year'] - 2000

        page = {"months": months, "categories": categories}
        page.update(page_conf)

        return render(request, "money/report.html", page)

class MoneyViewGraph(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'money/graph.html')
