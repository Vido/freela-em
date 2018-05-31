from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.DashboardIndex.as_view(), name='dashboard_index'),
    url(r'(?P<pk>[0-9]+)$', views.ClassInfoDetailView.as_view(),
        name='classinfo_detail'),
    url(r'(?P<pk>[0-9]+)/send_invoice$', views.ClassInfoSendInvoice.as_view(),
        name='classinfo_sendinvoice'),
    url(r'^base/', views.test_view, name='test_view'),
]
