
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if password == confirm_password:
                user = form.save(commit=False)
                user.set_password(password)

                # Every new registration is a normal candidate
                user.is_staff = False
                user.is_superuser = False

                user.save()

                messages.success(request, "Registration successful! Please login.")
                return redirect("login")
            else:
                messages.error(request, "Passwords do not match.")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})



def login_user(request):

    # If already logged in, redirect according to role
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect("dashboard")
        else:
            return redirect("candidate_dashboard")

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

            if user.is_staff or user.is_superuser:
                return redirect("dashboard")
            else:
                return redirect("candidate_dashboard")

        else:
            messages.error(request, "Invalid Username or Password.")

    # Important: This return must be outside the POST condition
    return render(request, "accounts/login.html")


def logout_user(request):
    logout(request)
    return redirect("login")
