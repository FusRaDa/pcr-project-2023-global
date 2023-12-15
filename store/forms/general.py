from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.affiliates import Brand
from ..models.items import Tag

class SearchStoreForm(forms.Form):
  kit_name = forms.CharField()

  cat_num = forms.CharField()

  brands = forms.ModelMultipleChoiceField(
    queryset=Brand.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  tags = forms.ModelMultipleChoiceField(
    queryset=Tag.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) 
    self.fields['brands'].widget.attrs['class'] = 'form-select'
    self.fields['tags'].widget.attrs['class'] = 'form-select'
    self.fields['kit_name'].widget.attrs['class'] = 'form-control'
    self.fields['cat_num'].widget.attrs['class'] = 'form-control'


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