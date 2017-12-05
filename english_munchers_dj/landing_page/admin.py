from django.contrib import admin
from .models import ClassRequest

@admin.register(ClassRequest)
class ClassRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'phone_number', 'email', 'ip_address', 'created_on')
    fields = ('name', 'id', 'phone_number', 'email', 'ip_address', 'created_on')
    readonly_fields=('id', 'created_on', 'ip_address')

admin.autodiscover()
