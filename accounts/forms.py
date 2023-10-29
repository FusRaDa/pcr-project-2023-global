from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CreateUserForm(UserCreationForm):
  class Meta: 
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class AssignRolesForm(ModelForm):
  class Meta:
    model = User
    fields = ['groups']


class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = '__all__'
    exclude = ['username', 'email'] 