from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from ..models.pcr import ThermalCyclerProtocol, Process


class ThermalCyclerProtocolForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) 
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['type'].widget.attrs['class'] = 'form-select'
    self.fields['denature_temp'].widget.attrs['class'] = 'form-control'
    self.fields['denature_duration'].widget.attrs['class'] = 'form-control'
    self.fields['anneal_temp'].widget.attrs['class'] = 'form-control'
    self.fields['anneal_duration'].widget.attrs['class'] = 'form-control'
    self.fields['extension_temp'].widget.attrs['class'] = 'form-control'
    self.fields['extension_duration'].widget.attrs['class'] = 'form-control'
    self.fields['number_of_cycles'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = ThermalCyclerProtocol
    exclude = ['user']


class ProcessForm(ModelForm):

  class Meta:
    model = Process
    exclude = ['user', 'samples']