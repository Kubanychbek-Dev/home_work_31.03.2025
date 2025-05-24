import string
import random

from django.shortcuts import reverse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import User
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm, UserForm
from .services import send_register_email, send_new_password


class UserRegisterView(CreateView):
    """Rendering the page to create a user account"""
    model = User
    form_class = UserRegisterForm
    template_name = "users/user_register.html"
    extra_context = {
        "title": "Зарегистрироваться"
    }

    def form_valid(self, form):
        user = form.save()
        send_register_email(user.email)
        return HttpResponseRedirect(reverse("users:user_login"))


class UserLoginView(LoginView):
    """Rendering the page to login"""
    form_class = UserLoginForm
    template_name = "users/user_login.html"
    extra_context = {
        "title": "Вход в аккаунт"
    }


class UserProfileView(UpdateView):
    """Show user profile"""
    model = User
    form_class = UserForm
    template_name = "users/user_profile_read_only.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data["title"] = f"Ваш профиль:  {self.get_object()}"
        return context_data


class UserUpdateView(UpdateView):
    """Displaying a page for editing user information"""
    model = User
    form_class = UserUpdateForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("users:user_profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data["title"] = f"Обновить профиль {self.get_object()}"
        return context_data


class UserPasswordChangeView(PasswordChangeView):
    """Displaying the user password change page"""
    form_class = UserChangePasswordForm
    template_name = "users/user_change_password.html"
    success_url = reverse_lazy("users:user_profile")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data["title"] = f"Изменить пароль {self.request.user}"
        return context_data


class UserLogoutView(LogoutView):
    """Logout"""
    template_name = "users/user_logout.html"
    extra_context = {
        "title": "Выход из аккаунта"
    }


@login_required(login_url="users:user_login")
def user_generate_new_password(request):
    new_password = "".join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse("dogs:index"))


class UserListView(LoginRequiredMixin, ListView):
    """Displaying a list of users"""
    model = User
    extra_context = {
        "title": "Все наши пользователи"
    }
    template_name = "users/users.html"
    paginate_by = 2


class UserDetailView(DetailView):
    """User Profile Display"""
    model = User
    template_name = "users/user_detail.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        user_object = context_data["object"]
        context_data["title"] = f"Профиль пользователя {user_object}"
        return context_data
