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
    email = models.EmailField(blank=True, null=True)
    time = models.CharField(max_length=8, choices=TIME_CHOICES, default='open')
    preferred_im = models.CharField(max_length=16, choices=IM_CHOICES, default='whatsapp')
    ip_address = models.GenericIPAddressField()
    created_on = models.DateTimeField(editable=False, auto_now_add=True)

    def __str__(self):
        return ' '.join([str(self.id), self.name, self.ip_address])

    def int_class_time(self):
        try:
            time = int(self.time)
        except ValueError:
            time = 15

        return time


class ClassInfo(models.Model):
    class_request = models.ForeignKey(ClassRequest, on_delete=models.CASCADE)
    pvt_send_timestamp = models.DateTimeField(editable=False, auto_now_add=True)
    teacher = models.CharField(max_length=128, default='')
    chat_id = models.IntegerField(default=0)

    q1_sent = models.DateTimeField(editable=False, blank=True, null=True)
    success = models.NullBooleanField(default=True)

    # TODO
    # Why not
    # prof
