from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.inventory import Ladder, Gel, Plate, Tube, Reagent, Location, Dye


class LocationForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super(LocationForm, self).__init__(*args, **kwargs)
    self.fields['name'].error_messages = {'max_length': "Location name is too long."}
    self.fields['name'].widget.attrs['placeholder'] = "Name of freezer, bin, drawer, etc..."

    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = Location
    exclude = ['user']


class LadderForm(ModelForm):
  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Ladder
    exclude = ['user', 'last_updated']


class EditLadderForm(ModelForm):
  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Ladder
    fields = ['amount', 'exp_date', 'location']
    exclude = ['user', 'last_updated']


class GelForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['size'].widget.attrs['class'] = 'form-select'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Gel
    exclude = ['user', 'last_updated']


class EditGelForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Plate
    fields = ['amount', 'exp_date', 'location']
    exclude = ['user', 'last_updated']


class DyeForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Dye
    exclude = ['user', 'last_updated']


class EditDyeForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Dye
    fields = ['amount', 'exp_date', 'location']
    exclude = ['user', 'last_updated']
    

class PlateForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['size'].widget.attrs['class'] = 'form-select'
    self.fields['type'].widget.attrs['class'] = 'form-select'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Plate
    exclude = ['user', 'last_updated']


class EditPlateForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Plate
    fields = ['amount', 'exp_date', 'location']
    exclude = ['user', 'last_updated']


class TubeForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)
    
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

    self.fields['name'].widget.attrs['placeholder'] = "General identification of tubes..."
    self.fields['brand'].widget.attrs['placeholder'] = "Brand/manufacturer of tubes..."
    self.fields['lot_number'].widget.attrs['placeholder'] = "Lot number of box..."
    self.fields['catalog_number'].widget.attrs['placeholder'] = "Catalog number of item..."
    
  class Meta:
    model = Tube
    exclude = ['user', 'last_updated']


class EditTubeForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Tube
    fields = ['amount', 'exp_date', 'location']
    exclude = ['user', 'last_updated']


class ReagentForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
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
        message="If reagent is for extraction, stock concentration is not needed."
      )

    if pcr_reagent != None and usage == Reagent.Usages.EXTRACTION:
      raise ValidationError(
        message="Leave PCR reagent type empty if reagent usage is for extraction."
      )
    
    if pcr_reagent == None and usage == Reagent.Usages.PCR:
      raise ValidationError(
        message="Select PCR reagent type if reagent usage is for PCR."
      )
    
    if pcr_reagent == Reagent.PCRReagent.WATER and (stock != None or unit != None):
      raise ValidationError(
        message="Water for PCR does not require concentration."
      )
    
    if pcr_reagent == Reagent.PCRReagent.POLYMERASE and (unit != Reagent.ConcentrationUnits.UNITS or stock == None):
      raise ValidationError(
        message="Polymerase must have a concentration unit of U/\u00B5L."
      )
    
    if pcr_reagent == Reagent.PCRReagent.GENERAL and unit == Reagent.ConcentrationUnits.UNITS:
      raise ValidationError(
        message="General PCR reagents cannot have a concentration unit of U/\u00B5L."
      )
    
    if pcr_reagent == Reagent.PCRReagent.GENERAL and (unit == None or stock == None):
      raise ValidationError(
        message="General PCR reagents must have a concentration."
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


class EditReagentForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['volume'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'
    self.fields['unit_volume'].widget.attrs['class'] = 'form-select'
  
  class Meta:
    model = Reagent
    fields = ['location', 'volume', 'exp_date', 'unit_volume']
    exclude = ['user', 'last_updated']