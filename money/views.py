from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date

from api.models import Payment, Category
from helpers.pagination import get_page


class MoneyView(LoginRequiredMixin, View):
    def get(self, request):
        all_payments = Payment.objects.all().order_by("-spent", "-id")
        categories = Category.objects.all().order_by("id")
        active_page = request.GET.get('page')

        payments, page_conf = get_page(all_payments, active_page)
        page = {'payments': payments, 'categories': categories, 'today': date.today().isoformat()}
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