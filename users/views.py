import string
import random

from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from .models import User
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm
from .services import send_register_email, send_new_password


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:user_login")
    template_name = "users/user_register.html"
    extra_context = {
        "title": "Create account"
    }

# def user_register_view(request):
#     form = UserRegisterForm(request.POST)
#     if request.method == "POST":
#         if form.is_valid():
#             new_user = form.save()
#             new_user.set_password(form.cleaned_data["password"])
#             new_user.save()
#             send_register_email(new_user.email)
#             return HttpResponseRedirect(reverse("users:user_login"))
#     context = {
#         "title": "Create account",
#         "form": UserRegisterForm
#     }
#     return render(request, "users/user_register.html", context=context)


def user_login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(email=cleaned_data["email"], password=cleaned_data["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("dogs:index"))
            return HttpResponse("Вы не зарегистрированы либо неверно введены данные")
    context = {
        "title": "Вход в аккаунт",
        "form": UserLoginForm
    }
    return render(request, "users/user_login.html", context=context)


@login_required(login_url="users:user_login")
def user_profile_view(request):
    user_object = request.user
    if user_object.first_name and user_object.last_name:
        user_name = f"{user_object.first_name} {user_object.last_name}"
    else:
        user_name = "Anonymous user"
    context = {
        "title": "Your Profile"
    }
    return render(request, "users/user_profile_read_only.html", context=context)


@login_required(login_url="users:user_login")
def user_update_view(request):
    user_object = request.user
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            user_object = form.save()
            user_object.save()
            return HttpResponseRedirect(reverse("users:user_profile"))
    context = {
        "object": user_object,
        "title": f"Изменить профиль: {user_object.first_name} {user_object.last_name}",
        "form": UserUpdateForm(instance=user_object)
    }
    return render(request, "users/user_update.html", context=context)


@login_required(login_url="users:user_login")
def user_change_password_view(request):
    user_object = request.user
    form = UserChangePasswordForm(user_object, request.POST)
    if request.method == "POST":
        if form.is_valid():
            user_object = form.save()
            update_session_auth_hash(request, user_object)
            messages.success(request, "Пароль успешно изменен")
            return HttpResponseRedirect(reverse("users:user_profile"))
        else:
            messages.error(request, "Не удалось изменить пароль")
    context = {
        "title": "Изменить пароль",
        "form": form
    }
    return render(request, "users/user_change_password.html", context=context)


@login_required(login_url="users:user_login")
def user_logout_view(request):
    logout(request)
    return redirect("dogs:index")


@login_required(login_url="users:user_login")
def user_generate_new_password(request):
    new_password = "".join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse("dogs:index"))