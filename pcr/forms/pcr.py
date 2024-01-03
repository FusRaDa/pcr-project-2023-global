from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

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

    array = []
    for sample in self.instance.samples.all():
      for assay in sample.assays.all():
        array.append(assay)
    assays = list(set(array))
    
    for assay in assays:
      if assay.type == Assay.Types.DNA and assay.method == Assay.Methods.PCR and pcr_dna_protocol == None:
        raise ValidationError(
          message="This process requires a protocol for DNA in PCR."
        )
      
      if assay.type == Assay.Types.RNA and assay.method == Assay.Methods.PCR and pcr_rna_protocol == None:
        raise ValidationError(
          message="This process requires a protocol for RNA in PCR."
        )
      
      if assay.type == Assay.Types.DNA and assay.method == Assay.Methods.qPCR and qpcr_dna_protocol == None:
        raise ValidationError(
          message="This process requires a protocol for DNA in qPCR."
        )
      
      if assay.type == Assay.Types.RNA and assay.method == Assay.Methods.qPCR and qpcr_rna_protocol == None:
        raise ValidationError(
          message="This process requires a protocol for RNA in qPCR."
        )
      
      if assay.method == Assay.Methods.PCR and not plate:
        raise ValidationError(
          message="This process requires plates for PCR"
        )
      
      if assay.method == Assay.Methods.PCR and not gel:
        raise ValidationError(
          message="This process requires gels for qPCR"
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


  class Meta:
    model = Process
    exclude = ['user', 'samples', 'is_processed', 'date_processed']