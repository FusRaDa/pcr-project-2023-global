from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField


class LoginUserForm(forms.Form):
  recaptcha = ReCaptchaField()
  username = forms.CharField(max_length=200, required=True)
  password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput())

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs['class'] = 'form-control'
    self.fields['username'].widget.attrs['id'] = 'username'
    self.fields['password'].widget.attrs['class'] = 'form-control'
    self.fields['password'].widget.attrs['id'] = 'password'

    self.fields['username'].widget.attrs['placeholder'] = 'Your username or email...'
    self.fields['password'].widget.attrs['placeholder'] = 'Your password...'


class CreateUserForm(UserCreationForm):
  recaptcha = ReCaptchaField()

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

    self.fields['username'].widget.attrs['placeholder'] = ''
    self.fields['first_name'].widget.attrs['placeholder'] = ''
    self.fields['last_name'].widget.attrs['placeholder'] = ''
    self.fields['email'].widget.attrs['placeholder'] = ''
    self.fields['password1'].widget.attrs['placeholder'] = ''
    self.fields['password2'].widget.attrs['placeholder'] = ''

  class Meta: 
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'recaptcha']

