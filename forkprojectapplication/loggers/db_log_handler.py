import json 
import logging

from django.contrib.auth import get_user_model
from django.utils import timezone

db_default_formatter = logging.Formatter()

sensitive_information = "password"

def remove_sensitive_information(request_dict):
    for key in sensitive_information:
        value = request_dict.get(key)
        if value is not None:
            request_dict[key] = ""
    
    return request_dict

def get_additional_information(request, request_log):
    if request.method == "GET":
        request_dict = remove_sensitive_information(request.GET.dict())
        request_log.parameters = json.dumps(request_dict)
    if request.method == "POST":
        request_dict = remove_sensitive_information(request.POST.dict())
        request_log.parameters = json.dumps(request_dict)
    
    return request_log

def get_request_information(request, request_log, user_model):
    request_log.url = "%s %s" % (request.method, request.get_full_path())

    request_log = get_additional_information(request, request_log)

    if request.session is not None:
        hijacker_history = request.session.get("hijack_history")
        if hijacker_history:
            hijacker_id = int(hijacker_history[0])
            hijacker = user_model.objects.get(id=hijacker_id)
            request_log.hijacker = hijacker.username
            request_log.hijacked = True
    
    return request_log

def handle_event(event, request_log):
    if event =="request_finished" or event == "request_failed":
        request_log.request_time_end = timezone.now() 

        if request_log.request_time_start:
            difference = request_log.request_time_end - request_log.request_time_start
            milliseconds = int(difference.total_seconds() * 1000)
            request_log.duration = milliseconds
        
    return request_log

def get_msg_information(msg, request_log):
    request_log.logger_name = msg["logger"]
    request_log.code = msg.get("code")
    request_log.ip_address = msg.get("ip")

    return request_log

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        from .models import RequestLog

        msg = record.msg
        user_model = get_user_model()

        request_log, created = RequestLog.objects.get_or_create(
            request_id=msg["request_id"]
        )
        print(request_log, created)

        if created:
            request_log.request_time_start = timezone.now()
        
        request_log = get_msg_information(msg, request_log)

        request = msg.get("request_object")
        print(request, request_log, ";;sd")
        if request:
            request_log = get_request_information(request, request_log, user_model)

        exception = msg.get("exception")
        if exception is not None:
            request_log.trace = exception
        
        user_id = msg.get("user_id")
        if user_id:
            user = user_model.objects.get(pk=user_id)
            request_log.user = user
            request_log.username = user.username

        event = msg.get("event")
        request_log = handle_event(event, request_log)

        if request_log.level == logging.NOTSET or request_log.level == logging.INFO:
            request_log.level = record.levelno
        
        request_log.save()
