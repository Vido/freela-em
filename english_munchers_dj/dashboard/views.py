from django.views.generic import ListView

from landing_page.models import ClassInfo
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardIndex(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard_index.html'
    model = ClassInfo
