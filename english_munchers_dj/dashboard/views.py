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
from django.shortcuts import render, get_object_or_404, redirect


class DashboardIndex(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard_index.html'
    model = ClassInfo

    def get_queryset(self, **kwargs):
        qs = super(DashboardIndex, self).get_queryset(**kwargs)

        initial_date = self.request.GET.get('date_start', '')
        final_date = self.request.GET.get('date_end', '')

        pending_invoices = self.request.GET.get('pending_invoices', False)
        success = self.request.GET.get('success', None)

        if initial_date:
            qs = qs.filter(pvt_send_timestamp__gte=initial_date)

        if final_date:
            qs = qs.filter(pvt_send_timestamp__lte=final_date)

        if success is not None:
            bool_dict = {'true': True, 'false': False}
            bool_success = bool_dict.get(success.lower(), False)
            qs = qs.filter(success=bool_success)

        if pending_invoices:
            qs = []
            for obj in qs:
                invoice = obj.get_invoice()
                if not invoice:
                    qs.append(obj)

        return qs


class InvoiceListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/paypalinvoice_list.html'
    model = PayPalInvoice

    def get_queryset(self, **kwargs):
        qs = super(InvoiceListView, self).get_queryset(**kwargs)

        initial_date = self.request.GET.get('date_start', '')
        final_date = self.request.GET.get('date_end', '')

        if initial_date:
            qs = qs.filter(created_on__gte=initial_date)

        if final_date:
            qs = qs.filter(final_on__gte=final_date)

        return qs

class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/paypalinvoice_detail.html'
    model = PayPalInvoice

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context['cached_inv'] = self.object.get_invoice()
        return context


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher

    def get_context_data(self, **kwargs):
        context = super(TeacherDetailView, self).get_context_data(**kwargs)

        initial_date = self.request.GET.get('date_start', None)
        final_date = self.request.GET.get('date_end', None)

        context['classinfo_list'] = self.object.get_classes(
                initial_date=initial_date,
                final_date=final_date)

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

def test_view(request):
    return render(request, "dashboard/base.html")
