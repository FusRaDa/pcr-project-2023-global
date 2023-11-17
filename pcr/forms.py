from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from .models import *
from .constants import *


# **INVENTORY** #
class LocationForm(ModelForm):
  class Meta:
    model = Location
    exclude = ['user']


class PlateForm(ModelForm):
  class Meta:
    model = Plate
    exclude = ['user', 'last_updated']


class TubeForm(ModelForm):
  class Meta:
    model = Tube
    exclude = ['user', 'last_updated']


class ReagentForm(ModelForm):
  class Meta:
    model = Reagent
    exclude = ['user', 'last_updated']
# INVENTORY #


# EXTRACTION #
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
    self.fields['reagents'].queryset = Reagent.objects.filter(user=self.user)
    
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
# EXTRACTION #


# ASSAY #
class FlourescenceForm(ModelForm):
  class Meta:
    model = Flourescence
    exclude = ['user']


class ControlForm(ModelForm):
  class Meta:
    model = Control
    exclude = ['user']


class AssayForm(ModelForm):
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
    self.fields['assays'].queryset = Assay.objects.filter(user=self.user)

  class Meta:
    model = AssayCode
    exclude = ['user']
# ASSAY #


# SAMPLE #
class BatchForm(ModelForm):

  code = forms.ModelChoiceField(
    queryset=None,
    widget=forms.RadioSelect,
    required=True)
  
  extraction_protocol = forms.ModelChoiceField(
    queryset=None,
    widget=forms.RadioSelect,
    required=True)
  
  def clean(self):
    cleaned_data = super().clean()
    lab_id = cleaned_data.get('lab_id')
    extraction_protocol = cleaned_data.get('extraction_protocol')
    code = cleaned_data.get('code')

    if Batch.objects.filter(user=self.user, lab_id=lab_id).exists():
      raise ValidationError(
        message='Batch with the same Lab ID already exists. Please change Lab ID.',
        )
    
    num = Batch.objects.filter(user=self.user).count() + 1
    if num > BATCH_LIMIT:
      raise ValidationError(
        message="You have reached the number of batches you can create.",
      )
    
    protocol_type = ExtractionProtocol.objects.get(name=extraction_protocol).type
    assays = AssayCode.objects.get(name=code).assays.all()

    if protocol_type != ExtractionProtocol.Types.TOTAL_NUCLEIC:
      incompatible = []
      for assay in assays:
        if assay.type != protocol_type:
          incompatible.append(assay)
          raise ValidationError(
            message=f'Extraction Protocol type: {protocol_type} is not compatible for assays: {incompatible} in code: {code}',
          )

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['code'].queryset = AssayCode.objects.filter(user=self.user)
    self.fields['extraction_protocol'].queryset = ExtractionProtocol.objects.filter(user=self.user)

  class Meta:
    model = Batch
    exclude = ['user', 'date_performed']


class SampleForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super(SampleForm, self).__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = Sample
    fields = ['sample_id']
    exclude = ['batch']


class SampleAssayForm(ModelForm):

  assays = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['assays'].queryset = Assay.objects.filter(user=self.user)

  class Meta:
    model = Sample
    fields = ['assays']
# SAMPLE #


# PROCESS #





