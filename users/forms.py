from django import forms
from .models import User
from .validators import validate_password
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        validate_password(cleaned_data["password1"])
        if cleaned_data["password1"] != cleaned_data["password2"]:
            raise forms.ValidationError("Does not match")
        return cleaned_data["password2"]


class UserForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "avatar",)


# class UserLoginForm(StyleFormMixin, forms.Form):
#     email = forms.EmailField(label="Email", required=True)
#     password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(attrs={
#         "placeholder": "Your password",
#         "class": "password",
#         "id": "password"
#     }))


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "avatar",)


class UserChangePasswordForm(StyleFormMixin, PasswordChangeForm):
    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch"
            )
        password_validation.validate_password(password2, self.user)
        return password2