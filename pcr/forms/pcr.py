from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from ..models.pcr import ThermalCyclerProtocol, Process
from ..models.inventory import Plate, Gel
from ..models.assay import Assay


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

  plate = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  gel = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  def clean(self):
    cleaned_data = super().clean()
    pcr_dna_protocol = cleaned_data.get('pcr_dna_protocol')
    pcr_rna_protocol = cleaned_data.get('pcr_rna_protocol')
    qpcr_dna_protocol = cleaned_data.get('qpcr_dna_protocol')
    qpcr_rna_protocol = cleaned_data.get('qpcr_rna_protocol')
    plate = cleaned_data.get('plate')
    gel = cleaned_data.get('gel')
    min_samples = cleaned_data.get('min_samples')

    array = []
    for sample in self.instance.samples.all():
      for assay in sample.assays.all():
        array.append(assay)
    assays = list(set(array))

    req_pcr_dna_protocol = False
    req_pcr_rna_protocol = False
    req_qpcr_dna_protocol = False
    req_qpcr_rna_protocol = False
    req_plates = False
    req_gels = False

    for assay in assays:
      if assay.type == Assay.Types.DNA and assay.method == Assay.Methods.PCR:
        req_pcr_dna_protocol = True
      if assay.type == Assay.Types.RNA and assay.method == Assay.Methods.PCR:
        req_pcr_rna_protocol = True
      if assay.type == Assay.Types.DNA and assay.method == Assay.Methods.qPCR:
        req_qpcr_dna_protocol = True
      if assay.type == Assay.Types.RNA and assay.method == Assay.Methods.qPCR:
        req_qpcr_rna_protocol = True
      if assay.method == Assay.Methods.qPCR:
        req_plates = True
      if assay.method == Assay.Methods.PCR:
        req_gels = True

    if req_pcr_dna_protocol and not pcr_dna_protocol:
      raise ValidationError(
        message="This process requires a thermal cycler protocol for DNA in PCR."
      )
    
    if req_pcr_rna_protocol and not pcr_rna_protocol:
      raise ValidationError(
        message="This process requires a thermal cycler protocol for RNA in PCR."
      )
    
    if req_qpcr_dna_protocol and not qpcr_dna_protocol:
      raise ValidationError(
        message="This process requires a thermal cycler protocol for DNA in qPCR."
      )
    
    if req_qpcr_rna_protocol and not qpcr_rna_protocol:
      raise ValidationError(
        message="This process requires a thermal cycler protocol for RNA in qPCR."
      )
    
    if req_plates and not plate:
      raise ValidationError(
        message="This process requires plates."
      )
    
    if req_gels and not gel:
      raise ValidationError(
        message="This process requires gels."
      )
    
    if req_plates and plate:
      plates = []
      for p in plate.all().order_by('size'):
        plates.append(p.size)
      min_num = plates[0]

      for assay in assays:
        if min_samples > min_num - assay.controls.count():
          raise ValidationError(
            message=f"Minimum samples per plate cannot exceed {min_num - assay.controls.count()}"
          )
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['plate'].queryset = Plate.objects.filter(user=self.user)
    self.fields['gel'].queryset = Gel.objects.filter(user=self.user)

    self.fields['pcr_dna_protocol'].widget.attrs['class'] = 'form-select'
    self.fields['pcr_rna_protocol'].widget.attrs['class'] = 'form-select'
    self.fields['qpcr_dna_protocol'].widget.attrs['class'] = 'form-select'
    self.fields['qpcr_rna_protocol'].widget.attrs['class'] = 'form-select'

    self.fields['min_samples_per_plate'].widget.attrs['class'] = 'form-control'
    self.fields['min_samples_per_gel'].widget.attrs['class'] = 'form-control'

    self.fields['min_samples_per_plate'].widget.attrs['min'] = 0
    self.fields['min_samples_per_gel'].widget.attrs['min'] = 0

  class Meta:
    model = Process
    exclude = ['user', 'samples', 'is_processed', 'date_processed']