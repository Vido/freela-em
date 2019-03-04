import logging
import json

from django.shortcuts import render
import pagseguro import Payment

#from .models import PayPalInvoice

from . import sandbox


def send_invoice(invoice_dict, class_info_id):
    logging.basicConfig(level=logging.INFO)

    pagamento = Payment(email=u'emaildasuaconta@dominio.tld', token='seutokendeaacessocom32caracteres')
    pagamento.add_item(item_id=u'id-do-item-1', description=u'Desc. do produto', amount=7, quantity=2)
    pagamento.set_client(name=u'Adam Yauch', phone_area_code=11, phone_number=12341234, cpf='93537621701')
    pagamento.set_shipping(cost=1.2)

    try:
        pagamento.request()
    except Exception as e:
        return

    url = pagamento.payment_url

#    if pp_response:
#        r = json.dumps(invoice.to_dict(), sort_keys=False, indent=4)
#        PayPalInvoice.objects.create(
#                invoice_id=invoice['id'],
#                invoice_json=invoice.to_dict(),
#                class_info_id=class_info_id)
#
#        invoice.send()
#
#    else:
#        r = invoice.error
#        PayPalInvoice.objects.create(
#                success=False,
#                invoice_id=invoice['id'],
#                invoice_json=json.dumps(invoice),
#                class_info_id=class_info_id)

    print(url)
    return url
