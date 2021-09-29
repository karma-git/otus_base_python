from django.forms import ModelForm

from blog.models import Author

from django.core.exceptions import ValidationError

import re


class AnimalCreateForm(ModelForm):
    class Meta:
        model = Author
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form_control"
            print(name, field)
            # print(dir(field.widget))

    def clean_email(self):
        """
        validate email address
        """
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        email = self.cleaned_data["email"]
        if not re.fullmatch(regex, email):
            raise ValidationError("email invalid")

        return email
