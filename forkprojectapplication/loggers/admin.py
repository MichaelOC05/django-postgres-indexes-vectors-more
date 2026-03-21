from django.contrib import admin
from forkprojectapplication.loggers.models import RequestLog
from django.utils.html import format_html

# Register your models here.
class RequestLogAdmin(admin.ModelAdmin):
    list_display = (
        "level",
        "code",
        "get_user_email",
        "request_time_start",
        "short_url",
        "ip_address",
        "duration",
        "url"
    )
    list_display_links = (
        "level",
    )

    list_filter = (
        "level",
    )

    search_fields = ["trace", "email_address", "url"]

    def traceback(self, instance):
        return format_html(
            "<pre><code>{content}</code></pre>",
            content=instance.trace if instance.trace else ""
        )

    def get_user_email(self, obj):
        return obj.email_address
    
admin.site.register(RequestLog, RequestLogAdmin)