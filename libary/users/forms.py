from django import forms
from django.forms import ModelForm, ChoiceField, ValidationError
from .models import DefaultUser
from django.contrib.auth.forms import (
    UserCreationForm as UserCreationFormGeneric,
    AuthenticationForm,
)


class CreateUserForm(UserCreationFormGeneric):
    class Meta:
        model = DefaultUser
        fields = ["name", "password1", "password2"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if name:
            if len(name.split(" ")) != 3:
                raise ValidationError(
                    "Ошибка записи ФИО. Верный пример: Иванов Иван Иванович"
                )
        else:
            raise ValidationError(
                "Ошибка записи ФИО. Верный пример: Иванов Иван Иванович"
            )
        return name


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs) -> None:
        super().__init__(request, *args, **kwargs)
        self.fields["username"] = forms.ChoiceField(
            choices=[
                (user.username, user.last_name) for user in DefaultUser.objects.all()
            ]
        )
        # (значение, отображаемое имя)
