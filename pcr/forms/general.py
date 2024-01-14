from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.assay import AssayCode


class SearchProcessForm(forms.Form):
  panel = forms.ModelChoiceField(queryset=None, required=False)

  lab_id = forms.CharField(max_length=4, required=False)

  start_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  end_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date End',
    required=False)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['panel'].queryset = AssayCode.objects.filter(user=self.user)

    self.fields['panel'].widget.attrs['class'] = 'form-select'
    self.fields['lab_id'].widget.attrs['class'] = 'form-control'
    self.fields['start_date'].widget.attrs['class'] = 'form-control'
    self.fields['end_date'].widget.attrs['class'] = 'form-control'


class DeletionForm(forms.Form):

  confirm = forms.CharField()

  def __init__(self, *args, **kwargs):
    self.value = kwargs.pop('value')
    super().__init__(*args, **kwargs) 
    self.fields['confirm'].widget.attrs['class'] = 'form-control'
    
  def clean(self):
    cleaned_data = super().clean()
    confirm = cleaned_data.get('confirm')
    if confirm != self.value:
      raise ValidationError(
        message="Invalid value entered, please try again."
      )