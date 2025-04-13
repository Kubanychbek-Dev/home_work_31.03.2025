from django import forms
from .models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UserRegisterForm(StyleFormMixin, forms.ModelForm):
    password = forms.CharField(label="", required=True, widget=forms.PasswordInput(attrs={
        "placeholder": "Your password",
        "class": "password",
        "id": "password"
    }))
    password2 = forms.CharField(label="", required=True, widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password",
        "class": "confirm-password",
        "id": "confirm-password"
    }))

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data["password"] != cleaned_data["password2"]:
            raise forms.ValidationError("Does not match")
        return cleaned_data["password2"]


class UserLoginForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(label="", required=True)
    password = forms.CharField(label="", required=True, widget=forms.PasswordInput(attrs={
        "placeholder": "Your password",
        "class": "password",
        "id": "password"
    }))
