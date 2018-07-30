import json
import math

from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import FormView
from django.template import Template, Context
from django.template.loader import render_to_string

from django.urls import reverse

from dashboard.models import Teacher
from dashboard.models import Teacher
from dashboard.forms import InvoiceForm

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


class ClassInfoSendInvoice(LoginRequiredMixin, FormView):
    template_name = 'dashboard/classinfo_sendinvoice.html'
    fields = ['teacher']
    form_class = InvoiceForm

    def get_object(self):
        queryset = ClassInfo.objects.all()
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        else:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_success_url(self):
        return reverse('dashboard_index')

    def get_initial(self):
        try:
            obj = self.get_object()
            quant = math.ceil(float(obj.class_length)/15.0)
        except:
            quant = 0

        context = {
            'quant': quant,
            'price': 10,
        }

        return context

    def form_valid(self, form):
        price = form.cleaned_data['price']
        quant = form.cleaned_data['quant']
        pk = self.kwargs.get('pk', None)

        invoice_dict = json.loads(
                self.get_invoice_json(quant, price))
        self.paypal_invoice_send(invoice_dict, pk)
        return super().form_valid(form)

    def paypal_invoice_send(self, invoice_dict, pk):
        from paypal_integration.views import send_invoice
        r = send_invoice(invoice_dict, pk)
        return r

    def get_invoice_json(self, quant, price):
        context = {
                'quant': quant,
                'price': price,
        }
        invoice_json = render_to_string('paypal_integration/invoice.json',
                context)
        print(invoice_json)
        return invoice_json

    def get_context_data(self, **kwargs):
        context = super(ClassInfoSendInvoice, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['object'] = obj
        context['cached_inv'] = obj.get_invoice()
        return context

def test_view(request):
    return render(request, "dashboard/base.html")
