from django.urls import path
from forkprojectapplication.common import views

urlpatterns = [
    path("", views.index, name="index"),
]
