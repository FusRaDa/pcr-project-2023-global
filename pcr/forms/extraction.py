from typing import Any
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.inventory import Tube, Reagent
from ..models.extraction import ExtractionProtocol, TubeExtraction, ReagentExtraction, Step


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

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['amount_per_sample'].widget.attrs['class'] = 'form-control'
    self.fields['order'].widget.attrs['class'] = 'form-control'

    self.fields['amount_per_sample'].error_messages = {'min_value': "Every tube should be used at least once per sample."}

  class Meta:
    model = TubeExtraction
    exclude = ['tube', 'protocol']


class ReagentExtractionForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['amount_per_sample'].widget.attrs['class'] = 'form-control'
    self.fields['order'].widget.attrs['class'] = 'form-control'

    self.fields['amount_per_sample'].error_messages = {'min_value': "Every reagent should have a volume per sample."}

  class Meta:
    model = ReagentExtraction
    exclude = ['reagent', 'protocol']


class StepForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['number'].widget.attrs['class'] = 'form-control'
    self.fields['number'].widget.attrs['min'] = 1
    self.fields['instruction'].widget.attrs['class'] = 'form-control'
    self.fields['instruction'].widget.attrs['placeholder'] = 'Instructions...'

  class Meta:
    model = Step
    exclude = ['protocol']