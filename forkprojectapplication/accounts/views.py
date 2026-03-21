from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm  # Import your custom forms


def login_signup_view(request):
    if request.method == "POST":
        print(request.POST)
        if "login" in request.POST:
            login_form = LoginForm(request.POST)
            signup_form = SignupForm()

            if login_form.is_valid():
                username = login_form.cleaned_data.get("username")
                password = login_form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    return redirect("index")

        elif "signup" in request.POST:
            login_form = LoginForm()
            signup_form = SignupForm(request.POST)
            print(signup_form.is_valid())
            if signup_form.is_valid():
                signup_form.save()
                username = signup_form.cleaned_data.get("username")
                password = signup_form.cleaned_data.get("password1")
                user = authenticate(username=username, password=password)
                print(user)

                if user is not None:
                    login(request, user)
                    return redirect("index")
    else:
        login_form = LoginForm()
        signup_form = SignupForm()

    return render(
        request,
        "login_signup.html",
        {"login_form": login_form, "signup_form": signup_form},
    )


def logout_view(request):
    logout(request)
    return redirect("login-page")
