from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.assay import Assay, AssayCode, ReagentAssay, Fluorescence, Control
from ..models.inventory import Reagent, Location


class FluorescenceForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) 
    self.fields['name'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Fluorescence
    exclude = ['user']


class ControlForm(ModelForm):

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
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'
    
  class Meta:
    model = Control
    exclude = ['user']


class AssayForm(ModelForm):

  fluorescence = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)
  
  controls = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)
  
  reagents = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)
  
  def clean(self):
    cleaned_data = super().clean()
    reaction_volume = cleaned_data.get('reaction_volume')
    sample_volume = cleaned_data.get('sample_volume')

    if reaction_volume < sample_volume:
      raise ValidationError(
        message="Reaction volume must be greater or equal to the sample volume."
      )

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['fluorescence'].queryset = Fluorescence.objects.filter(user=self.user)
    self.fields['controls'].queryset = Control.objects.filter(user=self.user)
    self.fields['reagents'].queryset = Reagent.objects.filter(user=self.user, usage=Reagent.Usages.PCR)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['method'].widget.attrs['class'] = 'form-select'
    self.fields['type'].widget.attrs['class'] = 'form-select'
    self.fields['sample_volume'].widget.attrs['class'] = 'form-control'
    self.fields['reaction_volume'].widget.attrs['class'] = 'form-control'
    
  class Meta:
    model = Assay
    exclude = ['user']


class ReagentAssayForm(ModelForm):
  class Meta:
    model = ReagentAssay
    exclude = ['reagent', 'assay']


class AssayCodeForm(ModelForm):

  assays = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True,)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['assays'].queryset = Assay.objects.filter(user=self.user).order_by('name')
    self.fields['name'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = AssayCode
    exclude = ['user']