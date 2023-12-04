from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.inventory import Plate, Tube, Reagent, Location


class LocationForm(ModelForm):

  name = forms.CharField(
    widget=forms.TextInput(attrs={'placeholder': 'Storage area such as a freezer or cabinet...'})
  )

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
  
  exp_date = forms.DateField(
      widget=forms.DateInput(attrs={'type': 'date'}),
      label='Date Start',
      required=False)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)
    
    self.fields['location'].error_messages = {'required': "Select the storage location of this reagent."}

    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['size'].widget.attrs['class'] = 'form-select'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Plate
    exclude = ['user', 'last_updated']


class TubeForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)
  
  exp_date = forms.DateField(
      widget=forms.DateInput(attrs={'type': 'date'}),
      label='Date Start',
      required=False)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)
    
    self.fields['location'].error_messages = {'required': "Select the storage location of this reagent."}

    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Tube
    exclude = ['user', 'last_updated']


class ReagentForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)
  
  exp_date = forms.DateField(
      widget=forms.DateInput(attrs={'type': 'date'}),
      label='Date Start',
      required=False)
  
  def clean(self):
    cleaned_data = super().clean()
    stock = cleaned_data.get('stock_concentration')
    unit = cleaned_data.get('unit_concentration')
    pcr_reagent = cleaned_data.get('pcr_reagent')
    usage = cleaned_data.get('usage')

    if usage == Reagent.Usages.EXTRACTION and (stock != None or unit != None):
      raise ValidationError(
        {'usage': ["If reagent is for extraction, stock concentration is not needed."]}
      )

    if stock != None and unit == None:
      raise ValidationError(
        {'unit_concentration': ["Don't forget to assign a concentration unit to your stock concentration."]}
      )
    
    if stock == None and unit != None:
      raise ValidationError(
        {'unit_concentration': ["Leave unit concentration blank if a stock concentration is not needed."]}
      )
    
    if pcr_reagent != None and usage == Reagent.Usages.EXTRACTION:
      raise ValidationError(
        {'pcr_reagent': ["Leave PCR reagent type empty if reagent usage is for extraction."]}
      )
    
    if pcr_reagent == None and usage == Reagent.Usages.PCR:
      raise ValidationError(
        {'pcr_reagent': ["Select PCR reagent type if reagent usage is for PCR."]}
      )
    
    if pcr_reagent == Reagent.PCRReagent.WATER and (stock != None or unit != None):
      raise ValidationError(
        {'pcr_reagent': ["Water for PCR does not require concentration."]}
      )
    
    if pcr_reagent == Reagent.PCRReagent.POLYMERASE and unit != Reagent.ConcentrationUnits.UNITS:
      raise ValidationError(
        message="Polymerase must have a concentration unit of U/\u00B5L."
      )
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['location'].error_messages = {'required': "Select the storage location of this reagent."}

    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['usage'].widget.attrs['class'] = 'form-select'
    self.fields['pcr_reagent'].widget.attrs['class'] = 'form-select'
    self.fields['volume'].widget.attrs['class'] = 'form-control'
    self.fields['unit_volume'].widget.attrs['class'] = 'form-select'
    self.fields['stock_concentration'].widget.attrs['class'] = 'form-control'
    self.fields['unit_concentration'].widget.attrs['class'] = 'form-select'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'
  
  class Meta:
    model = Reagent
    exclude = ['user', 'last_updated']