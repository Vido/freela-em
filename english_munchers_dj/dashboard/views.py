from django.views.generic import ListView
from django.views.generic import DetailView

from landing_page.models import ClassInfo
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardIndex(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard_index.html'
    model = ClassInfo


class ClassInfoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/classinfo_detail.html'
    model = ClassInfo


class ClassInfoSendInvoice(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/classinfo_sendinvoice.html'
    model = ClassInfo

