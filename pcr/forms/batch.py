from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..custom.constants import BATCH_LIMIT
from ..models.extraction import ExtractionProtocol
from ..models.assay import Assay, AssayCode
from ..models.batch import Batch, Sample


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
  
  def clean(self):
    assays = self.cleaned_data.get('assays')
    sample = Sample.objects.get(user=self.user, pk=self.instance.pk)
    batch_type = sample.batch.extraction_protocol.type

    if batch_type != ExtractionProtocol.Types.TOTAL_NUCLEIC:
      incompatible = []
      for assay in assays:
        if assay.type != batch_type:
          incompatible.append(assay)
          raise ValidationError(
            message=f'Extraction Protocol: {batch_type} is not compatible for assays: {incompatible}',
          )

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['assays'].queryset = Assay.objects.filter(user=self.user)

  class Meta:
    model = Sample
    fields = ['assays']