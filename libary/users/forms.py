from django.forms import ModelForm,ChoiceField
from .models import  DefaultUser
from django.contrib.auth.forms import UserCreationForm as UserCreationFormGeneric

class CreateUserForm(UserCreationFormGeneric):
    class Meta:
        model = DefaultUser
        fields = ["username","password1","password2"]

class LoginUserForm(ModelForm):
    #users = [user.username for user in User.objects.all()]
    #user = ChoiceField(choices=[(username, username) for username in users])

    class Meta:
        model = DefaultUser
        fields = ["username"]






