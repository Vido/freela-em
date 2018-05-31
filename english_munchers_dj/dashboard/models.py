from django.db import models

# Create your models here.


class Teacher(models.Model):
    created_on = models.DateTimeField(editable=False, auto_now_add=True)
    teacher = models.CharField(max_length=128, default='', unique=True)

    def get_classes(self, success=None, initial_date=None, final_date=None):
        from landing_page.models import ClassInfo
        qs_classinfo = ClassInfo.objects.filter(teacher=self.teacher)

        if success is not None:
            qs_classinfo = qs_classinfo.filter(success=success)

        if initial_date is not None:
            qs_classinfo = qs_classinfo.filter(
                    pvt_send_timestamp__gte=initial_date)

        if final_date is not None:
            qs_classinfo = qs_classinfo.filter(
                    pvt_send_timestamp__lte=final_date)

        return qs_classinfo
