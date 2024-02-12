from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class SearchUserForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)

  CHOICES = [(None, '------'), (False, 'False'), (True, 'True')]

  staff = forms.ChoiceField(choices=CHOICES, required=False)
  active = forms.ChoiceField(choices=CHOICES, required=False)
  superuser = forms.ChoiceField(choices=CHOICES, required=False)
  can_review = forms.ChoiceField(choices=CHOICES, required=False)

  last_login_start = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  last_login_end = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date End',
    required=False)
  
  joined_login_start = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  joined_login_end = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date End',
    required=False)
 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) 
    self.fields['text_search'].widget.attrs['class'] = 'form-control'
    self.fields['staff'].widget.attrs['class'] = 'form-select'
    self.fields['active'].widget.attrs['class'] = 'form-select'
    self.fields['superuser'].widget.attrs['class'] = 'form-select'
    self.fields['can_review'].widget.attrs['class'] = 'form-select'
    self.fields['last_login_start'].widget.attrs['class'] = 'form-control'
    self.fields['last_login_end'].widget.attrs['class'] = 'form-control'
    self.fields['joined_login_start'].widget.attrs['class'] = 'form-control'
    self.fields['joined_login_end'].widget.attrs['class'] = 'form-control'
