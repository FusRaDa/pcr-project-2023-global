from typing import Any
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.inventory import Tube, Reagent
from ..models.extraction import ExtractionProtocol, TubeExtraction, ReagentExtraction


class ExtractionProtocolForm(ModelForm):

  tubes = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)
  
  reagents = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['tubes'].queryset = Tube.objects.filter(user=self.user)
    self.fields['reagents'].queryset = Reagent.objects.filter(user=self.user, usage=Reagent.Usages.EXTRACTION)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['type'].widget.attrs['class'] = 'form-select'
    self.fields['doc_url'].widget.attrs['class'] = 'form-control'

    self.fields['tubes'].error_messages = {'required': "Select tubes for your extraction protocol."}
    self.fields['reagents'].error_messages = {'required': "Select reagents for your extraction protocol."}
    
  class Meta:
    model = ExtractionProtocol
    exclude = ['user']


class TubeExtractionForm(ModelForm):

  def clean(self):
    cleaned_data = super().clean()
    amount_per_sample = cleaned_data.get('amount_per_sample')

    if amount_per_sample == None:
      raise ValidationError(
        message=f"{self.instance.tube.name} must be used at least once per sample"
      )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['amount_per_sample'].widget.attrs['class'] = 'form-control'
    self.fields['order'].widget.attrs['class'] = 'form-control'

    self.fields['amount_per_sample'].widget.attrs['min'] = 1
    self.fields['order'].widget.attrs['min'] = 0

  class Meta:
    model = TubeExtraction
    exclude = ['tube', 'protocol']


class ReagentExtractionForm(ModelForm):

  def clean(self):
    cleaned_data = super().clean()
    amount_per_sample = cleaned_data.get('amount_per_sample')

    if amount_per_sample == None:
      raise ValidationError(
        message=f"{self.instance.reagent.name} must have a volume per sample"
      )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['amount_per_sample'].widget.attrs['class'] = 'form-control'
    self.fields['order'].widget.attrs['class'] = 'form-control'

    self.fields['amount_per_sample'].widget.attrs['min'] = 1
    self.fields['order'].widget.attrs['min'] = 0

  class Meta:
    model = ReagentExtraction
    exclude = ['reagent', 'protocol']