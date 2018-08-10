from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.forms import ModelForm

from landing_page.models import ClassRequest

class ClassRequestForm(ModelForm):
    class Meta:
        model = ClassRequest
        fields = ['name', 'phone_number', 'email', 'time', 'preferred_im']

class IndexView(FormView):

    template_name = "landing_page/home.html"
    form_class = ClassRequestForm
    success_url = '/success'

    def form_valid(self, form):
        class_request_obj = form.save(commit=False)
        class_request_obj.ip_address = self.request.META['REMOTE_ADDR']
        class_request_obj.save()
        return super(IndexView, self).form_valid(form)


class SuccessView(TemplateView):
    template_name = "landing_page/success.html"

