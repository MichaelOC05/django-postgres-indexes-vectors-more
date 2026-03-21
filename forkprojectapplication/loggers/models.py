import logging
from django.db import models

from django.conf import settings
from django.template.defaultfilters import truncatechars
from django.utils.translation import gettext_lazy as _


USER_MODEL = settings.AUTH_USER_MODEL

# Create your models here.
LOG_LEVELS = (
    (logging.NOTSET, _("NotSet")),
    (logging.INFO, _("Info")),
    (logging.WARNING, _("Warning")),
    (logging.DEBUG, _("Debug")),
    (logging.ERROR, _("Error")),
    (logging.FATAL, _("Fatal")),
)


class RequestLog(models.Model):

    request_id = models.CharField(max_length=200, unique=True, null=True)

    code = models.CharField(max_length=100, null=True, default=4)

    logger_name = models.CharField(max_length=100)

    level = models.PositiveSmallIntegerField(

        choices=LOG_LEVELS, default=logging.NOTSET, db_index=True

    )

    msg = models.TextField()

    user = models.ForeignKey(

        USER_MODEL, null=True, related_name="User", on_delete=models.CASCADE

    )

    trace = models.TextField(blank=True, null=True)

    url = models.URLField(max_length=200, null=True)

    request_time_start = models.DateTimeField(null=True, verbose_name="Created at")

    request_time_end = models.DateTimeField(null=True)

    duration = models.IntegerField(null=True, verbose_name="Duration in ms")

    ip_address = models.CharField(max_length=25, null=True)

    email_address = models.EmailField(null=True)

    hijacker = models.CharField(max_length=40, null=True)

    parameters = models.TextField(null=True)

    hijacked = models.BooleanField(default=False)

 

    @property

    def short_url(self):

        return truncatechars(self.url, 50)

 

    def __str__(self):

        return self.msg

 

    # implemented in case a url is longer than 200 characters (which would exceed), was causing errors in testing

    def save(self, *args, **kwargs):

        if self.url is not None and len(self.url) > 200:

            self.url = self.url[:200]

        super().save(*args, **kwargs)

 

    class Meta:

        ordering = ("-request_time_start",)

        verbose_name = "Request Log"

        verbose_name_plural = "Request Logs"