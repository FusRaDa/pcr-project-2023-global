import re

from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.inventory import Ladder, Gel, Plate, Tube, Reagent, Location, Dye

from ..custom.constants import LIMITS


class LocationForm(ModelForm):

  def clean(self):
    cleaned_data = super().clean()
    name = cleaned_data.get('name')

    name_exists = Location.objects.filter(user=self.user, name=name).exists()
    if name_exists and self.instance.name != name:
      raise ValidationError(
        message=f"Location with the name: {name} already exists."
      )
    
    if Location.objects.filter(user=self.user).count() >= LIMITS.MAX_LOCATION_LIMIT and self.instance.pk == None:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_LOCATION_LIMIT} storage locations. Should you require more, please contact us!"
      )

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs)
    self.fields['name'].error_messages = {'max_length': "Location name is too long."}
    self.fields['name'].widget.attrs['class'] = 'form-control'

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
  
  def clean(self):
    if Ladder.objects.filter(user=self.user).count() >= LIMITS.MAX_LADDER_LIMIT and self.instance.pk == None:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_LADDER_LIMIT} ladders. Should you require more, please contact us!"
      )
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['threshold'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'
    self.fields['image'].widget.attrs['class'] = 'form-control'

    self.fields['amount'].widget.attrs['min'] = 0
    self.fields['threshold'].widget.attrs['min'] = 0

  class Meta:
    model = Ladder
    exclude = ['user', 'last_updated', 'threshold_diff', 'merged_lot_numbers']


class GelForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def clean(self):
    if Gel.objects.filter(user=self.user).count() >= LIMITS.MAX_GEL_LIMIT and self.instance.pk == None:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_GEL_LIMIT} gels. Should you require more, please contact us!"
      )
  
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
    self.fields['threshold'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

    self.fields['amount'].widget.attrs['min'] = 0
    self.fields['threshold'].widget.attrs['min'] = 0

  class Meta:
    model = Gel
    exclude = ['user', 'last_updated', 'threshold_diff', 'merged_lot_numbers']


class DyeForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def clean(self):
    if Dye.objects.filter(user=self.user).count() >= LIMITS.MAX_DYE_LIMIT and self.instance.pk == None:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_DYE_LIMIT} dyes. Should you require more, please contact us!"
      )
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['threshold'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

    self.fields['amount'].widget.attrs['min'] = 0
    self.fields['threshold'].widget.attrs['min'] = 0

  class Meta:
    model = Dye
    exclude = ['user', 'last_updated', 'threshold_diff', 'merged_lot_numbers']


class PlateForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def clean(self):
    if Plate.objects.filter(user=self.user).count() >= LIMITS.MAX_PLATE_LIMIT and self.instance.pk == None:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_PLATE_LIMIT} plates. Should you require more, please contact us!"
      )
  
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
    self.fields['threshold'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

    self.fields['amount'].widget.attrs['min'] = 0
    self.fields['threshold'].widget.attrs['min'] = 0

  class Meta:
    model = Plate
    exclude = ['user', 'last_updated', 'threshold_diff', 'merged_lot_numbers']


class TubeForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  def clean(self):
    if Tube.objects.filter(user=self.user).count() >= LIMITS.MAX_TUBE_LIMIT and self.instance.pk == None:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_TUBE_LIMIT} tubes. Should you require more, please contact us!"
      )

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)
    
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['threshold'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

    self.fields['amount'].widget.attrs['min'] = 0
    self.fields['threshold'].widget.attrs['min'] = 0

  class Meta:
    model = Tube
    exclude = ['user', 'last_updated', 'threshold_diff', 'merged_lot_numbers']


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
    forward_sequence = cleaned_data.get('forward_sequence')
    reverse_sequence = cleaned_data.get('reverse_sequence')
    mixture_volume = cleaned_data.get('mixture_volume_per_reaction')

    if Reagent.objects.filter(user=self.user).count() >= LIMITS.MAX_REAGENT_LIMIT and self.instance.pk == None:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_REAGENT_LIMIT} reagents. Should you require more, please contact us!"
      )

    if usage == Reagent.Usages.EXTRACTION and (stock != None or unit != None):
      raise ValidationError(
        message="If reagent is for extraction, stock concentration is not needed."
      )
    
    if usage == Reagent.Usages.EXTRACTION and mixture_volume:
      raise ValidationError(
        message="If reagent is for extraction, leave mixture volume per reaction empty."
      )

    if pcr_reagent != None and usage == Reagent.Usages.EXTRACTION:
      raise ValidationError(
        message="Leave PCR reagent type empty if reagent usage is for extraction."
      )
    
    if pcr_reagent == None and usage == Reagent.Usages.PCR:
      raise ValidationError(
        message="Select PCR reagent type if reagent usage is for PCR."
      )
    
    if (pcr_reagent == Reagent.PCRReagent.POLYMERASE and unit != Reagent.ConcentrationUnits.UNITS) or (pcr_reagent != Reagent.PCRReagent.POLYMERASE and unit == Reagent.ConcentrationUnits.UNITS):
      raise ValidationError(
        message="Polymerase reagents require a unit of U/\u00B5L. If your polymerase is in a different concentration, set PCR Reagent as General."
      )
    
    if mixture_volume > 0 and pcr_reagent != Reagent.PCRReagent.MIXTURE:
      raise ValidationError(
        message="Mixture volumes per reaction are required for reagents that are enzyme mixtures with no specified stock concentration."
      )
    
    if pcr_reagent == Reagent.PCRReagent.MIXTURE and not mixture_volume > 0:
      raise ValidationError(
        message="Reagents that are enzyme mixtures must have a volume per reaction set."
      )
    
    if pcr_reagent == Reagent.PCRReagent.MIXTURE and (stock != None or unit != None):
      raise ValidationError(
        message="Reagents that are mixtures do not need a stock concentration."
      )
    
    if pcr_reagent == Reagent.PCRReagent.WATER and (stock != None or unit != None):
      raise ValidationError(
        message="Water for PCR does not require concentration."
      )
  
    if usage == Reagent.Usages.PCR and pcr_reagent != Reagent.PCRReagent.WATER and pcr_reagent != Reagent.PCRReagent.MIXTURE and (stock == None or unit == None):
      raise ValidationError(
        message="All reagents for PCR except water must have a concentration."
      )
    
    if pcr_reagent != Reagent.PCRReagent.PRIMER and forward_sequence != None or pcr_reagent != Reagent.PCRReagent.PRIMER and reverse_sequence != None:
      raise ValidationError(
        message="Only primers require a sequence."
      )
    
    valid_seq = re.compile('[^GUACT]')
    if forward_sequence and valid_seq.search(forward_sequence.upper()) is not None:
      raise ValidationError(
        message="Forward sequence for primer contains invalid characters."
      )
    
    if reverse_sequence and valid_seq.search(reverse_sequence.upper()) is not None:
      raise ValidationError(
        message="Reverse sequence for primer contains invalid characters."
      )
    
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

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
    self.fields['forward_sequence'].widget.attrs['class'] = 'form-control'
    self.fields['reverse_sequence'].widget.attrs['class'] = 'form-control'
    self.fields['mixture_volume_per_reaction'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'

    self.fields['threshold'].widget.attrs['class'] = 'form-control'
    self.fields['threshold_unit'].widget.attrs['class'] = 'form-select'

    self.fields['volume'].widget.attrs['min'] = 0
    self.fields['stock_concentration'].widget.attrs['min'] = 0
    self.fields['threshold'].widget.attrs['min'] = 0
    self.fields['mixture_volume_per_reaction'].widget.attrs['min'] = 0
  
  class Meta:
    model = Reagent
    exclude = ['user', 'last_updated', 'threshold_diff', 'merged_lot_numbers']


# **MERGEABLE FORMS** #
class MergeItemsForm(forms.Form):
  confirm = forms.CharField()

  mergeable_items = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True,
    error_messages={'required': 'Please select at least one item to merge.'})
  
  def __init__(self, *args, **kwargs):
    self.value = kwargs.pop('value')
    self.mergeable_items = kwargs.pop('mergeable_items')
    super().__init__(*args, **kwargs) 
    self.fields['mergeable_items'].queryset = self.mergeable_items
    self.fields['confirm'].widget.attrs['class'] = 'form-control'

  def clean(self):
    cleaned_data = super().clean()
    confirm = cleaned_data.get('confirm')
    mergeable_items = cleaned_data.get('mergeable_items')

    for item in mergeable_items:
      if item.is_expired:
        raise ValidationError(
          message=f"{item} is expired."
        )
      
    if confirm != self.value:
      raise ValidationError(
        message="Invalid value entered, please try again."
      )
# **MERGEABLE FORMS** #