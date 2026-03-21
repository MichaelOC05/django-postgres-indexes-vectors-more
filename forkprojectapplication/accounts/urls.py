from django.urls import path
from forkprojectapplication.accounts import views

urlpatterns = [
    path("login_page/", views.login_signup_view, name="login-page"),
    path("logout/", views.logout, name="logout"),
]
