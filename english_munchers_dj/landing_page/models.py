from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _

TIME_CHOICES = (
    ('15', _('15 minutes')),
    ('30', _('30 minutes')),
    ('45', _('45 minutes')),
    ('60', _('60 minutes')),
    ('open', _('Open Time')),
)

IM_CHOICES = (
    ('whatsapp', _('WhatsAPP')),
    ('telegram', _('Telegram')),
    ('skype', _('Skype')),
    ('hangouts', _('Hangouts')),
)

class ClassRequest(models.Model):
    name = models.CharField(max_length=64)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone Number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    country = models.CharField(max_length=32)
    email = models.EmailField()
    time = models.CharField(max_length=8, choices=TIME_CHOICES, default='open')
    preferred_im = models.CharField(max_length=16, choices=IM_CHOICES, default='whatsapp')
    ip_address = models.GenericIPAddressField()
    created_on = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(ClassRequest, self).save(*args, **kwargs)
