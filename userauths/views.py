# userauths/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from core.models import (
    Vendor, Category, Product,
    Cart, CartItem, Wishlist,
    Order, OrderItem, Review,
    Address,PaymentMethod
)
User = get_user_model()

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered. Please use a different email.")
            else:
                # Create user but don't commit yet
                user = form.save(commit=False)
                user.is_staff = False        # ensure normal user
                user.is_superuser = False    # ensure normal user
                user.save()                  # save to DB
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect("home")  # Change to login page URL if needed
        else:
            # Collect and display all form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user using email as username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Check if user is admin/staff
            if user.is_staff or user.is_superuser:
                messages.error(request, "Admin users cannot log in here. Please use the admin panel.")
                return redirect("login")  # redirect back to login page

            # Normal user login
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, "login.html")



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")   # redirect to login page (change if needed)


