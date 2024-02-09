from typing import Any
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.inventory import Tube, Reagent
from ..models.extraction import ExtractionProtocol, TubeExtraction, ReagentExtraction


class ExtractionProtocolForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) 
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['type'].widget.attrs['class'] = 'form-select'
    self.fields['doc_url'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = ExtractionProtocol
    exclude = ['user', 'tubes', 'reagents']


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