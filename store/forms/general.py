from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.affiliates import Brand
from ..models.items import Tag

# combine all 4 forms into one for store
class SearchStoreForm(forms.Form):
  text_search = forms.CharField(required=False)

  price = forms.ChoiceField(choices=[('price', 'Ascending'), ('-price', 'Descending')], initial='Descending', required=True)

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
    self.fields['text_search'].widget.attrs['class'] = 'form-control'
    self.fields['price'].widget.attrs['class'] = 'form-select'


class ItemLotNumberForm(forms.Form):
  lot_number = forms.CharField(required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) 
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'


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