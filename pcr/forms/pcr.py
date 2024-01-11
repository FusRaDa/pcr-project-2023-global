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

    min_samples_per_plate_dna = cleaned_data.get('min_samples_per_plate_dna')
    min_samples_per_plate_rna = cleaned_data.get('min_samples_per_plate_rna')

    min_samples_per_gel_dna = cleaned_data.get('min_samples_per_gel_dna')
    min_samples_per_gel_rna = cleaned_data.get('min_samples_per_gel_rna')

    array = []
    for sample in self.instance.samples.all():
      for assay in sample.assays.all():
        array.append(assay)
    assays = list(set(array))

    pcr_dna_assays = []
    pcr_rna_assays = []
    qpcr_dna_assays = []
    qpcr_rna_assays = []

    for assay in assays:
      if assay.method == Assay.Methods.PCR and assay.type == Assay.Types.DNA:
        pcr_dna_assays.append(assay)
      if assay.method == Assay.Methods.PCR and assay.type == Assay.Types.RNA:
        pcr_rna_assays.append(assay)
      if assay.method == Assay.Methods.qPCR and assay.type == Assay.Types.DNA:
        qpcr_dna_assays.append(assay)
      if assay.method == Assay.Methods.qPCR and assay.type == Assay.Types.RNA:
        qpcr_rna_assays.append(assay)

    if len(pcr_dna_assays) > 0 and not pcr_dna_protocol:
      raise ValidationError(
        message="This process requires a thermal cycler protocol for DNA in PCR."
      )
    
    if len(pcr_rna_assays) > 0 and not pcr_rna_protocol:
      raise ValidationError(
        message="This process requires a thermal cycler protocol for RNA in PCR."
      )
    
    if len(qpcr_dna_assays) > 0 and not qpcr_dna_protocol:
      raise ValidationError(
        message="This process requires a thermal cycler protocol for DNA in qPCR."
      )
    
    if len(qpcr_rna_assays) > 0 and not qpcr_rna_protocol:
      raise ValidationError(
        message="This process requires a thermal cycler protocol for RNA in qPCR."
      )
    
    if len(qpcr_dna_assays) > 0 and not plate or len(qpcr_rna_assays) > 0 and not plate:
      raise ValidationError(
        message="This process requires plates."
      )
    
    if len(pcr_dna_assays) and not gel or len(pcr_rna_assays) and not gel:
      raise ValidationError(
        message="This process requires gels."
      )
    
    if len(qpcr_dna_assays) > 0 and plate:
      plates = []
      for p in plate.all().order_by('size'):
        plates.append(p.size)
      min_num = plates[0]

      for assay in qpcr_dna_assays:
        if min_samples_per_plate_dna > min_num - assay.controls.count():
          raise ValidationError(
            message=f"Minimum samples (DNA) per plate cannot exceed {min_num - assay.controls.count()}"
          )
        
    if len(qpcr_rna_assays) > 0 and plate:
      plates = []
      for p in plate.all().order_by('size'):
        plates.append(p.size)
      min_num = plates[0]

      for assay in qpcr_rna_assays:
        if min_samples_per_plate_rna > min_num - assay.controls.count():
          raise ValidationError(
            message=f"Minimum samples (RNA) per plate cannot exceed {min_num - assay.controls.count()}"
          )
        
    if len(pcr_dna_assays) and gel:
      gels = []
      for g in gel.all().order_by('size'):
        gels.append(g.size)
      min_num = gels[0]

      for assay in pcr_dna_assays:
        if min_samples_per_gel_dna > min_num - assay.controls.count():
          raise ValidationError(
            message=f"Minimum samples per gel cannot exceed {min_num - assay.controls.count()}"
          )
        
    if len(pcr_rna_assays) and gel:
      gels = []
      for g in gel.all().order_by('size'):
        gels.append(g.size)
      min_num = gels[0]

      for assay in pcr_rna_assays:
        if min_samples_per_gel_rna > min_num - assay.controls.count():
          raise ValidationError(
            message=f"Minimum samples per gel cannot exceed {min_num - assay.controls.count()}"
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

    self.fields['min_samples_per_plate_dna'].widget.attrs['class'] = 'form-control'
    self.fields['min_samples_per_plate_rna'].widget.attrs['class'] = 'form-control'
    self.fields['min_samples_per_gel_dna'].widget.attrs['class'] = 'form-control'
    self.fields['min_samples_per_gel_rna'].widget.attrs['class'] = 'form-control'

    self.fields['min_samples_per_plate_dna'].widget.attrs['min'] = 0
    self.fields['min_samples_per_plate_rna'].widget.attrs['min'] = 0
    self.fields['min_samples_per_gel_dna'].widget.attrs['min'] = 0
    self.fields['min_samples_per_gel_rna'].widget.attrs['min'] = 0

  class Meta:
    model = Process
    exclude = ['user', 'samples', 'is_processed', 'date_processed', 'pcr_dna_json', 'pcr_rna_json', 'qpcr_dna_json', 'qpcr_rna_json']