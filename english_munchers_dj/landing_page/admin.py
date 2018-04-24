from django.contrib import admin
from .models import ClassRequest
from .models import ClassInfo

@admin.register(ClassRequest)
class ClassRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'phone_number', 'email', 'ip_address', 'created_on')
    fields = ('name', 'id', 'phone_number', 'email', 'ip_address', 'created_on')
    readonly_fields=('id', 'created_on', 'ip_address')


@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'pvt_send_timestamp')
    fields = ('class_request', 'teacher', 'chat_id',
            'success', 'reason_why', 'proof')


admin.autodiscover()
