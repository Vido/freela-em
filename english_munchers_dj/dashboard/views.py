import json

from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.template import Template, Context
from django.template.loader import render_to_string

from django.urls import reverse

from dashboard.models import Teacher
from landing_page.models import ClassInfo
from paypal_integration.models import PayPalInvoice
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardIndex(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard_index.html'
    model = ClassInfo


class InvoiceListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/paypalinvoice_list.html'
    model = PayPalInvoice


class TeachersListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/paypalinvoice_list.html'
    model = Teacher

    #def get_context_data(self, **kwargs):
    #    context = super(InvoiceDetailView, self).get_context_data(**kwargs)
    #    context['teachers_list'] = self.object.get_invoice()
    #    return context


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/paypalinvoice_detail.html'
    model = PayPalInvoice

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context['cached_inv'] = self.object.get_invoice()
        return context


class ClassInfoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/classinfo_detail.html'
    model = ClassInfo


class ClassInfoSendInvoice(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/classinfo_sendinvoice.html'
    model = ClassInfo
    fields = ['teacher']

    def get_success_url(self):
        return reverse('dashboard_index')

    def form_valid(self, form):
        from paypal_integration.views import send_invoice
        invoice_dict = json.loads(self.get_invoice_json())
        send_invoice(invoice_dict, self.object.pk)
        return super().form_valid(form)

    def get_invoice_json(self):
        invoice_json = render_to_string('paypal_integration/invoice.json', {})
        print(invoice_json)
        return invoice_json

    def get_context_data(self, **kwargs):
        context = super(ClassInfoSendInvoice, self).get_context_data(**kwargs)
        context['invoice_json'] = self.get_invoice_json()
        return context
