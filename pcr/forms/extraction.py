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
    
  class Meta:
    model = ExtractionProtocol
    exclude = ['user']


class TubeExtractionForm(ModelForm):

  class Meta:
    model = TubeExtraction
    exclude = ['tube', 'protocol']


class ReagentExtractionForm(ModelForm):

  class Meta:
    model = ReagentExtraction
    exclude = ['reagent', 'protocol']