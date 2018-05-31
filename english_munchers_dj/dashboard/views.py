from django.views.generic import ListView
from django.views.generic import DetailView
from django.template import Template, Context
from django.template.loader import render_to_string

from landing_page.models import ClassInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

class DashboardIndex(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard_index.html'
    model = ClassInfo


class ClassInfoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/classinfo_detail.html'
    model = ClassInfo


class ClassInfoSendInvoice(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/classinfo_sendinvoice.html'
    model = ClassInfo

    def get_context_data(self, **kwargs):
        context = super(ClassInfoSendInvoice, self).get_context_data(**kwargs)
        invoice_json = render_to_string('paypal_integration/invoice.json', {})
        print(invoice_json)
        context['invoice_json'] = invoice_json
        return context

def test_view(request):
    return render(request, "dashboard/base.html")
