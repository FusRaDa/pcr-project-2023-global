from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _

from ..models.inventory import Plate, Tube, Reagent, Location


class LocationForm(ModelForm):
  
  def __init__(self, *args, **kwargs):
    super(LocationForm, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = Location
    exclude = ['user']


class PlateForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['size'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Plate
    exclude = ['user', 'last_updated']


class TubeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super(TubeForm, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = Tube
    exclude = ['user', 'last_updated']


class ReagentForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super(ReagentForm, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = Reagent
    exclude = ['user', 'last_updated']