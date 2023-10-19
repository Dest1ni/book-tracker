from django import forms
from django.forms import ModelForm,ChoiceField
from .models import  DefaultUser
from django.contrib.auth.forms import UserCreationForm as UserCreationFormGeneric,AuthenticationForm

class CreateUserForm(UserCreationFormGeneric):
    class Meta:
        model = DefaultUser
        fields = ["name","password1","password2"]

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs) -> None:
        super().__init__(request, *args, **kwargs)
        self.fields['username'] = forms.ChoiceField(choices=[(user.username,user.last_name) for user in DefaultUser.objects.all()])
        #(значение, отображаемое имя)




