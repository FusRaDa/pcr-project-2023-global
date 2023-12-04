from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CreateUserForm(UserCreationForm):

  def clean(self):
    cleaned_data = super().clean()
    email = cleaned_data.get('email')

    if not email:
      raise ValidationError(
        ({'email': ["Please enter an email."]})
      )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['email'].required = True

  class Meta: 
    model = User
    fields = ['username', 'email', 'password1', 'password2']

