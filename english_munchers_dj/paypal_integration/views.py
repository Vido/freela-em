import logging
import json

from django.shortcuts import render
from paypalrestsdk import Invoice

from .models import PayPalInvoice

from . import sandbox

def send_invoice(invoice_dict, class_info_id):
    logging.basicConfig(level=logging.INFO)
    invoice = Invoice(invoice_dict)

    try:
        pp_response = invoice.create()
    except Exception as e:
        return

    if pp_response:
        r = json.dumps(invoice.to_dict(), sort_keys=False, indent=4)
        PayPalInvoice.objects.create(
                invoice_id=invoice['id'],
                invoice_json=invoice.to_dict(),
                class_info_id=class_info_id)

        invoice.send()

    else:
        r = invoice.error
        PayPalInvoice.objects.create(
                success=False,
                invoice_id=invoice['id'],
                invoice_json=json.dumps(invoice),
                class_info_id=class_info_id)

    print(r)
    return r
