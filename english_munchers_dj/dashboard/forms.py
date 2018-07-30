from django import forms

class InvoiceForm(forms.Form):
    price = forms.IntegerField(label='Value per time slice',
            help_text='(BRL/15min)')
    quant = forms.IntegerField(label='Time slices')
