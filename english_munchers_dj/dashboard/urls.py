from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.DashboardIndex.as_view(), name='dashboard_index'),
]
