from django.forms import ModelForm

from store.models import Customer

from django.core.exceptions import ValidationError

import re


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        email = self.cleaned_data["email"]
        if not re.fullmatch(regex, email):
            raise ValidationError("email invalid")
        return email
