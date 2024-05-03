from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
import re

from ..models.items import Kit, StorePlate, StoreTube, StoreReagent, Tag, Review, StoreGel, StoreDye, StoreLadder, StoreControl
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
    self.fields['description'].widget.attrs['class'] = 'form-control'
    self.fields['catalog_number'].widget.attrs['class'] = 'form-control'
    self.fields['price'].widget.attrs['class'] = 'form-control'
    self.fields['affiliate_link'].widget.attrs['class'] = 'form-control'
    self.fields['image'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Kit
    fields = '__all__'


class StoreGelForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['size'].widget.attrs['class'] = 'form-select'
    self.fields['amount'].widget.attrs['class'] = 'form-control'

    self.fields['amount'].widget.attrs['min'] = 0

  class Meta:
    model = StoreGel
    exclude = ['kit']


class StorePlateForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['size'].widget.attrs['class'] = 'form-select'
    self.fields['type'].widget.attrs['class'] = 'form-select'
    self.fields['amount'].widget.attrs['class'] = 'form-control'

    self.fields['amount'].widget.attrs['min'] = 0

  class Meta:
    model = StorePlate
    exclude = ['kit']


class StoreTubeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'

    self.fields['amount'].widget.attrs['min'] = 0

  class Meta:
    model = StoreTube
    exclude = ['kit']


class StoreControlForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'

    self.fields['amount'].widget.attrs['min'] = 0

  class Meta:
    model = StoreControl
    exclude = ['kit']


class StoreLadderForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'

    self.fields['amount'].widget.attrs['min'] = 0

  class Meta:
    model = StoreLadder
    exclude = ['kit']


class StoreDyeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'

    self.fields['amount'].widget.attrs['min'] = 0

  class Meta:
    model = StoreDye
    exclude = ['kit']

class StoreReagentForm(ModelForm):

  def clean(self):
    cleaned_data = super().clean()
    stock = cleaned_data.get('stock_concentration')
    unit = cleaned_data.get('unit_concentration')
    pcr_reagent = cleaned_data.get('pcr_reagent')
    usage = cleaned_data.get('usage')
    forward_sequence = cleaned_data.get('forward_sequence')
    reverse_sequence = cleaned_data.get('reverse_sequence')
    mixture_volume = cleaned_data.get('mixture_volume_per_reaction')

    if usage == StoreReagent.Usages.EXTRACTION and (stock != None or unit != None):
      raise ValidationError(
        message="If reagent is for extraction, stock concentration is not needed."
      )

    if pcr_reagent != None and usage == StoreReagent.Usages.EXTRACTION:
      raise ValidationError(
        message="Leave PCR reagent type empty if reagent usage is for extraction."
      )
    
    if pcr_reagent == None and usage == StoreReagent.Usages.PCR:
      raise ValidationError(
        message="Select PCR reagent type if reagent usage is for PCR."
      )
    
    if pcr_reagent == StoreReagent.PCRReagent.POLYMERASE and unit != StoreReagent.ConcentrationUnits.UNITS:
      raise ValidationError(
        message="Polymerase reagents require a unit of U/\u00B5L. If your polymerase is in a different concentration, set PCR Reagent as General."
      )
    
    if mixture_volume and pcr_reagent != StoreReagent.PCRReagent.MIXTURE:
      raise ValidationError(
        message="Mixture volumes per reaction are required for reagents that are enzyme mixtures with no specified stock concentration."
      )
    
    if pcr_reagent == StoreReagent.PCRReagent.MIXTURE and not mixture_volume:
      raise ValidationError(
        message="Reagents that are enzyme mixtures must have a volume per reaction used."
      )
    
    if pcr_reagent == StoreReagent.PCRReagent.WATER and (stock != None or unit != None):
      raise ValidationError(
        message="Water for PCR does not require concentration."
      )
  
    if usage == StoreReagent.Usages.PCR and pcr_reagent != StoreReagent.PCRReagent.WATER and pcr_reagent != StoreReagent.PCRReagent.MIXTURE and (stock == None or unit == None):
      raise ValidationError(
        message="All reagents for PCR except water must have a concentration."
      )
    
    if pcr_reagent != StoreReagent.PCRReagent.PRIMER and forward_sequence != None or pcr_reagent != StoreReagent.PCRReagent.PRIMER and reverse_sequence != None:
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
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['usage'].widget.attrs['class'] = 'form-control'
    self.fields['pcr_reagent'].widget.attrs['class'] = 'form-select'
    self.fields['volume'].widget.attrs['class'] = 'form-control'
    self.fields['unit_volume'].widget.attrs['class'] = 'form-select'
    self.fields['stock_concentration'].widget.attrs['class'] = 'form-control'
    self.fields['unit_concentration'].widget.attrs['class'] = 'form-select'
    self.fields['forward_sequence'].widget.attrs['class'] = 'form-control'
    self.fields['reverse_sequence'].widget.attrs['class'] = 'form-control'
    self.fields['mixture_volume_per_reaction'].widget.attrs['class'] = 'form-control'

    self.fields['volume'].widget.attrs['min'] = 0
    self.fields['stock_concentration'].widget.attrs['min'] = 0
    self.fields['mixture_volume_per_reaction'].widget.attrs['min'] = 0

  class Meta:
    model = StoreReagent
    exclude = ['kit']


class ReviewForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['text'].widget.attrs['class'] = 'form-control'
    self.fields['rating'].widget.attrs['class'] = 'form-control'
    self.fields['rating'].widget.attrs['min'] = 0
    self.fields['rating'].widget.attrs['max'] = 5

  class Meta:
    model = Review
    exclude = ['kit', 'user', 'is_reported', 'date_updated']