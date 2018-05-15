from django.db import models
from django.contrib.postgres.fields import JSONField

class PayPalInvoice(models.Model):
    class_info_id = models.IntegerField(null=True, blank=True)
    invoice_id = models.CharField(max_length=36,null=True, blank=True)
    invoice_json = JSONField()
