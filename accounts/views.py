from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if password == confirm_password:

                user = form.save(commit=False)

                user.set_password(password)

                user.save()

                return redirect("dashboard")

    else:

        form = RegisterForm()

    context = {
        "form": form
    }

    return render(request, "accounts/register.html", context)

def login_user(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/")

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(request, "accounts/login.html")

def logout_user(request):

    logout(request)

    return redirect("login")