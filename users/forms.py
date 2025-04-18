from django import forms
from .models import User
from .validators import validate_password
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm


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
    pass