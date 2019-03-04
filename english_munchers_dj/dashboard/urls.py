from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.DashboardIndex.as_view(), name='dashboard_index'),

    url(r'invoices/$', views.InvoiceListView.as_view(), name='invoice_list'),
    url(r'invoice/(?P<pk>[0-9]+)$', views.InvoiceDetailView.as_view(),
        name='invoice_detail'),

    url(r'teachers/$', views.TeacherListView.as_view(), name='teacher_list'),
    url(r'teacher/(?P<pk>[0-9]+)$', views.TeacherDetailView.as_view(),
        name='teacher_detail'),

    url(r'prices/$', views.PricesFormView.as_view(), name='price_form'),

    url(r'(?P<pk>[0-9]+)$', views.ClassInfoDetailView.as_view(),
        name='classinfo_detail'),
    url(r'(?P<pk>[0-9]+)/send_invoice$', views.ClassInfoSendInvoice.as_view(),
        name='classinfo_sendinvoice'),
]
