from django import forms

class InvoiceForm(forms.Form):

    GATEWAYS = (
        ('Paypal', 'Paypal'),
        #('PagSeguro', 'PagSeguro'),
    )

    gateway = forms.ChoiceField(choices=GATEWAYS,
            required=True, label='Payments Gateway')
    price = forms.IntegerField(label='Value per time slice',
            help_text='(BRL/15min)')
    quant = forms.IntegerField(label='Time slices')
