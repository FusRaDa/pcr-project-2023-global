from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from ..models.items import Kit, StorePlate, StoreTube, StoreReagent, Tag, Review
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
    self.fields['image'].widget.attrs['class'] = 'form-control'

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

  def clean(self):
    cleaned_data = super().clean()
    stock = cleaned_data.get('stock_concentration')
    unit = cleaned_data.get('unit_concentration')
    pcr_reagent = cleaned_data.get('pcr_reagent')
    usage = cleaned_data.get('usage')

    if usage == StoreReagent.Usages.EXTRACTION and (stock != None or unit != None):
      raise ValidationError(
        {'usage': ["If reagent is for extraction, stock concentration is not needed."]}
      )

    if stock != None and unit == None:
      raise ValidationError(
        message="Don't forget to assign a concentration unit to your stock concentration."
      )
    
    if stock == None and unit != None:
      raise ValidationError(
        message="Leave unit concentration blank if a stock concentration is not needed."
      )
    
    if pcr_reagent != None and usage == StoreReagent.Usages.EXTRACTION:
      raise ValidationError(
        message="Leave PCR reagent type empty if reagent usage is for extraction."
      )
    
    if pcr_reagent == None and usage == StoreReagent.Usages.PCR:
      raise ValidationError(
        message="Select PCR reagent type if reagent usage is for PCR."
      )
    
    if pcr_reagent == StoreReagent.PCRReagent.WATER and (stock != None or unit != None):
      raise ValidationError(
        message="Water for PCR does not require concentration."
      )
    
    if pcr_reagent == StoreReagent.PCRReagent.POLYMERASE and unit != StoreReagent.ConcentrationUnits.UNITS:
      raise ValidationError(
        message="Polymerase must have a concentration unit of U/\u00B5L."
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
    exclude = ['kit', 'user', 'flags']