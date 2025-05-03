from django import forms
from .models import Dog, DogParent
from users.forms import StyleFormMixin


class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        # fields = "__all__"
        exclude = ("owner", "is_active", "views",)


class  DogAdminForm(DogForm):
    class Meta:
        model = Dog
        exclude = ("is_active",)


class DogParentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = DogParent
        fields = "__all__"