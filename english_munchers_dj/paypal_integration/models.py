from django.db import models
from django.contrib.postgres.fields import JSONField

from paypalrestsdk import Invoice, ResourceNotFound

class PayPalInvoice(models.Model):
    class_info_id = models.IntegerField(null=True, blank=True)
    invoice_id = models.CharField(max_length=36,null=True, blank=True)
    invoice_json = JSONField(null=True, blank=True)
    success = models.NullBooleanField(default=True)
    created_on = models.DateTimeField(editable=False, auto_now_add=True)

    def get_classinfo(self):
        from landing_page.models import ClassInfo
        return ClassInfo.objects.get(pk=self.class_info_id)

    def get_classrequest(self):
        return self.get_classinfo().class_request

    def get_invoice(self):
        from . import sandbox
        inv = Invoice.find(self.invoice_id)
        return inv
