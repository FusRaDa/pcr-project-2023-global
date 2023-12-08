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
        ({'email': ["Please enter an email."]})
      )
    
    if not first_name:
      raise ValidationError(
        ({'first_name': ["Please enter your first name."]})
      )
    
    if not last_name:
      raise ValidationError(
        ({'last_name': ["Please enter your last name."]})
      )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['email'].required = True
    self.fields['first_name'].required = True
    self.fields['last_name'].required = True

  class Meta: 
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

