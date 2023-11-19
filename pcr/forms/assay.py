from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _

from ..models.assay import Assay, AssayCode, ReagentAssay, Flourescence, Control


class FlourescenceForm(ModelForm):
  class Meta:
    model = Flourescence
    exclude = ['user']


class ControlForm(ModelForm):
  class Meta:
    model = Control
    exclude = ['user']


class AssayForm(ModelForm):

  flourescence = forms.ModelMultipleChoiceField(
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

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['flourescence'].queryset = Flourescence.objects.filter(user=self.user)
    self.fields['controls'].queryset = Flourescence.objects.filter(user=self.user)
    self.fields['reagents'].queryset = Flourescence.objects.filter(user=self.user)

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
    required=True)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['assays'].queryset = Assay.objects.filter(user=self.user).order_by('type')

  class Meta:
    model = AssayCode
    exclude = ['user']