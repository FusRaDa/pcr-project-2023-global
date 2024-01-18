from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django.utils.translation import gettext_lazy as _


class CreateUserForm(UserCreationForm):

  def clean(self):
    cleaned_data = super().clean()
    email = cleaned_data.get('email')
    first_name = cleaned_data.get('first_name')
    last_name = cleaned_data.get('last_name')

    if not email:
      raise ValidationError(
        message="Please enter an email."
      )
    
    if not first_name:
      raise ValidationError(
        message="Please enter your first name."
      )
    
    if not last_name:
      raise ValidationError(
        message="Please enter your last name."
      )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['email'].required = True
    self.fields['first_name'].required = True
    self.fields['last_name'].required = True

    self.fields['username'].widget.attrs['class'] = 'form-control'
    self.fields['username'].widget.attrs['id'] = 'username'

    self.fields['first_name'].widget.attrs['class'] = 'form-control'
    self.fields['first_name'].widget.attrs['id'] = 'first_name'

    self.fields['last_name'].widget.attrs['class'] = 'form-control'
    self.fields['last_name'].widget.attrs['id'] = 'last_name'

    self.fields['email'].widget.attrs['class'] = 'form-control'
    self.fields['email'].widget.attrs['id'] = 'email'

    self.fields['password1'].widget.attrs['class'] = 'form-control'
    self.fields['password1'].widget.attrs['id'] = 'password1'

    self.fields['password2'].widget.attrs['class'] = 'form-control'
    self.fields['password2'].widget.attrs['id'] = 'password2'

    self.fields['username'].widget.attrs['placeholder'] = 'Your unique username...'
    self.fields['first_name'].widget.attrs['placeholder'] = 'Your first name...'
    self.fields['last_name'].widget.attrs['placeholder'] = 'Your last name...'
    self.fields['email'].widget.attrs['placeholder'] = 'Your email...'
    self.fields['password1'].widget.attrs['placeholder'] = 'Enter password...'
    self.fields['password2'].widget.attrs['placeholder'] = 'Enter password again...'

  class Meta: 
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

