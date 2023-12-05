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
  
  extraction_protocol_dna = forms.ModelChoiceField(
    queryset=None,
    widget=forms.RadioSelect(attrs={"name": "extraction_protocol"}),
    required=False)
  
  extraction_protocol_rna = forms.ModelChoiceField(
    queryset=None,
    widget=forms.RadioSelect(attrs={"name": "extraction_protocol"}),
    required=False)

  extraction_protocol_tn = forms.ModelChoiceField(
    queryset=None,
    widget=forms.RadioSelect(attrs={"name": "extraction_protocol"}),
    required=False)
  
  def clean(self):
    cleaned_data = super().clean()
    
    num = Batch.objects.filter(user=self.user).count() + 1
    if num > BATCH_LIMIT:
      raise ValidationError(
        message="You have reached the number of batches you can create.",
      )
    
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['code'].queryset = AssayCode.objects.filter(user=self.user)
    self.fields['extraction_protocol_dna'].queryset = ExtractionProtocol.objects.filter(user=self.user, type=ExtractionProtocol.Types.DNA)
    self.fields['extraction_protocol_rna'].queryset = ExtractionProtocol.objects.filter(user=self.user, type=ExtractionProtocol.Types.RNA)
    self.fields['extraction_protocol_tn'].queryset = ExtractionProtocol.objects.filter(user=self.user, type=ExtractionProtocol.Types.TOTAL_NUCLEIC)

   

    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['number_of_samples'].widget.attrs['class'] = 'form-control'
    self.fields['lab_id'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Batch
    exclude = ['user', 'date_performed']


class DeleteBatchForm(forms.Form):

  confirm = forms.CharField()

  def __init__(self, *args, **kwargs):
    self.value = kwargs.pop('value')
    super().__init__(*args, **kwargs) 
    self.fields['confirm'].widget.attrs['class'] = 'form-control'
    
  def clean(self):
    cleaned_data = super().clean()
    confirm = cleaned_data.get('confirm')
    if confirm != self.value:
      raise ValidationError(
        message="Invalid batch name entered, please try again."
      )


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