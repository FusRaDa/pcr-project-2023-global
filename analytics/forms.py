from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import User


class SearchUserForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)

  CHOICES = [(None, '------'), (False, 'False'), (True, 'True')]

  is_staff = forms.ChoiceField(choices=CHOICES, required=False)
  is_active = forms.ChoiceField(choices=CHOICES, required=False)
  is_superuser = forms.ChoiceField(choices=CHOICES, required=False)
  can_review = forms.ChoiceField(choices=CHOICES, required=False)
  is_subscribed = forms.ChoiceField(choices=CHOICES, required=False)
  
  last_login_start = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  last_login_end = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date End',
    required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) 
    self.fields['text_search'].widget.attrs['class'] = 'form-control'
    self.fields['is_staff'].widget.attrs['class'] = 'form-select'
    self.fields['is_active'].widget.attrs['class'] = 'form-select'
    self.fields['is_superuser'].widget.attrs['class'] = 'form-select'
    self.fields['can_review'].widget.attrs['class'] = 'form-select'
    self.fields['is_subscribed'].widget.attrs['class'] = 'form-select'
    self.fields['last_login_start'].widget.attrs['class'] = 'form-control'
    self.fields['last_login_end'].widget.attrs['class'] = 'form-control'


class SearchLoginListForm(forms.Form):
  start_date = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  end_date = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date End',
    required=False)
  

class ManageUserForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    self.fields['can_review'].widget.attrs['class'] = 'form-control'
    self.fields['is_active'].widget.attrs['class'] = 'form-control'
    self.fields['is_staff'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = User
    fields = ['can_review', 'is_active', 'is_staff']
