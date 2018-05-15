from paypalrestsdk import Invoice
import logging
import json

from django.shortcuts import render

#import sandbox

def send_invoice(invoice_json):
    logging.basicConfig(level=logging.INFO)
    invoice = Invoice(invoice_json)
    if invoice.create():
        print(json.dumps(invoice.to_dict(), sort_keys=False, indent=4))
    else:
        print(invoice.error)

