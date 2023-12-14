from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from ..models.items import Kit, StorePlate, StoreTube, StoreReagent, Tag
from ..models.affiliates import Brand


class TagForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Tag
    fields = '__all__'

class KitForm(ModelForm):

  brand = forms.ModelChoiceField(
    queryset=Brand.objects.all(),
    widget=forms.RadioSelect,
    required=True)
  
  tags = forms.ModelMultipleChoiceField(
    queryset=Tag.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['price'].widget.attrs['class'] = 'form-control'
    self.fields['affiliate_link'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Kit
    fields = '__all__'


class StorePlateForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['size'].widget.attrs['class'] = 'form-select'
    self.fields['amount'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = StorePlate
    exclude = ['kit']


class StoreTubeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = StoreTube
    exclude = ['kit']


class StoreReagentForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['usage'].widget.attrs['class'] = 'form-control'
    self.fields['pcr_reagent'].widget.attrs['class'] = 'form-select'
    self.fields['volume'].widget.attrs['class'] = 'form-control'
    self.fields['unit_volume'].widget.attrs['class'] = 'form-select'
    self.fields['stock_concentration'].widget.attrs['class'] = 'form-control'
    self.fields['unit_concentration'].widget.attrs['class'] = 'form-select'

  class Meta:
    model = StoreReagent
    exclude = ['kit']