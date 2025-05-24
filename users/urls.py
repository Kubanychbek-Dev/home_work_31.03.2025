from django.urls import path
from users.apps import UsersConfig
from .views import (UserRegisterView, UserLoginView, UserProfileView, UserLogoutView, UserUpdateView,
                    UserPasswordChangeView, user_generate_new_password, UserListView, UserDetailView)

app_name = UsersConfig.name

urlpatterns = [
    path("", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("update/", UserUpdateView.as_view(), name="user_update"),
    path("change_password/", UserPasswordChangeView.as_view(), name="user_change_password"),
    path("profile/genpassword/", user_generate_new_password, name="user_generate_new_password"),

    path("all_users/", UserListView.as_view(), name="users_list"),
    path("profile/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
]
