import structlog

from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse

from forkprojectapplication.exampleapp.utils import generate_xlsx

 

struct_logger = structlog.get_logger("django_request_logger")




def generate_excel_request_logs(queryset):

    fields = [

        "code",

        "logger_name",

        "level",

        "url",

        "ip_address",

        "email_address",

        "parameters",

        "request_time_start",

        "duration",

        "hijacker",

        "hijacked",

        "trace",

        "parameters",

    ]

    queryset_dict = queryset.values(*fields)

 

    column_headers = [

        "Code",

        "Logger Name",

        "Level",

        "URL",

        "IP Address",

        "Email Address",

        "Parameters",

        "Created DateTime",

        "Duration",

        "Hijacker",

        "Hijacked",

        "Trace",

        "Parameters",

    ]

 

    return generate_xlsx(queryset_dict, column_headers)

 

def generate_excel_audit_logs(queryset):

    fields = [        

        "timestamp",

        "content_type",

        "object_repr",

        "action",

        "actor",

        "remote_addr",

        "was_hijacked",

        "hijacker_email",

        "additional_data",

        "changes",

    ]

   

    queryset_dict = queryset.values(*fields)

 

    column_headers = [

        "Created",

        "Content Type",

        "Object Representation",

        "Action",

        "Actor",

        "IP Address",

        "Hijacked",

        "Hijacker",

        "Additional Data",

        "Changes",

    ]

 

    return generate_xlsx(queryset_dict, column_headers, audit_logger=True)

 

def exception_handler_decorator(view_func):

    def wrapper(*args, **kwargs):

        try:

            return view_func(*args, **kwargs)

 

        except ObjectDoesNotExist as e:

            struct_logger.exception(e)

            response = HttpResponse("Error Occurred")

            response.status_code = 404

            return response

 

        except Exception as e:

            struct_logger.exception(e)

            response = HttpResponse("Error Occurred")

            response.status_code = 500

            return response

 

    return wrapper

