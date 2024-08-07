from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from ..models.pcr import ThermalCyclerProtocol, Process
from ..models.inventory import Plate, Gel
from ..models.assay import Assay

from ..custom.constants import LIMITS


class ThermalCyclerProtocolForm(ModelForm):

  def clean(self):
    cleaned_data = super().clean()
    name = cleaned_data.get('name')

    name_exists = ThermalCyclerProtocol.objects.filter(user=self.user, name=name).exists()
    if name_exists and self.instance.name != name:
      raise ValidationError(
        message=f"Thermal cycler protocol with the name: {name} already exists."
      )
    
    if ThermalCyclerProtocol.objects.filter(user=self.user).count() >= LIMITS.MAX_THERMAL_CYCLER_PROTOCOL_LIMIT and self.instance.pk == None:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_THERMAL_CYCLER_PROTOCOL_LIMIT} thermal cycler protocols. Should you require more, please contact us!"
      )

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
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

    self.fields['denature_temp'].widget.attrs['min'] = 0
    self.fields['denature_duration'].widget.attrs['min'] = 0
    self.fields['anneal_temp'].widget.attrs['min'] = 0
    self.fields['anneal_duration'].widget.attrs['min'] = 0
    self.fields['extension_temp'].widget.attrs['min'] = 0
    self.fields['extension_duration'].widget.attrs['min'] = 0
    self.fields['number_of_cycles'].widget.attrs['min'] = 0

  class Meta:
    model = ThermalCyclerProtocol
    exclude = ['user']


class ProcessForm(ModelForm):
  name = forms.CharField(required=False)

  qpcr_plate = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  pcr_plate = forms.ModelMultipleChoiceField(
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
    pcr_plate = cleaned_data.get('pcr_plate')
    qpcr_plate = cleaned_data.get('qpcr_plate')
    gel = cleaned_data.get('gel')

    if not self.user.is_subscribed:
      if Process.objects.filter(user=self.user, is_processed=True).count() >= LIMITS.PROCESS_LIMIT:
        raise ValidationError(
          message=f"You have reached the maximum number of {LIMITS.PROCESS_LIMIT} PCR processes. Consider upgrading for an infinite amount or deleting all processes."
        )
      
    if Process.objects.filter(user=self.user, is_processed=True).count() >= LIMITS.MAX_PROCESS_LIMIT:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_PROCESS_LIMIT} processes. Should you require more, please contact us!"
      )

    min_samples_per_plate_dna_qpcr = cleaned_data.get('min_samples_per_plate_dna_qpcr')
    min_samples_per_plate_rna_qpcr = cleaned_data.get('min_samples_per_plate_rna_qpcr')

    min_samples_per_plate_dna_pcr = cleaned_data.get('min_samples_per_plate_dna_pcr')
    min_samples_per_plate_rna_pcr = cleaned_data.get('min_samples_per_plate_rna_pcr')

    min_samples_per_gel = cleaned_data.get('min_samples_per_gel')

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

    # **VALIDATE PROTOCOLS** #
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
    # **VALIDATE PROTOCOLS** #
    
    # **VALIDATE qPCR PLATES** #
    if len(qpcr_dna_assays) > 0 and not qpcr_plate or len(qpcr_rna_assays) > 0 and not qpcr_plate:
      raise ValidationError(
        message="This process requires plates for qPCR."
      )
    # **VALIDATE qPCR PLATES** #
    
    # **VALIDATE PCR PLATES AND GELS** #
    if len(pcr_dna_assays) and not pcr_plate or len(pcr_rna_assays) and not pcr_plate:
      raise ValidationError(
        message="This process requires plates for PCR."
      )
    
    if len(pcr_dna_assays) and not gel or len(pcr_rna_assays) and not gel:
      raise ValidationError(
        message="This process requires gels for PCR."
      )
    # **VALIDATE PCR PLATES AND GELS** #
    
    # **VALIDATE qPCR PLATE MIN NUM** #
    if len(qpcr_dna_assays) > 0 and qpcr_plate:
      plates = []
      for p in qpcr_plate.all().order_by('size'):
        plates.append(p.size)
      min_num = plates[0]

      for assay in qpcr_dna_assays:
        if min_samples_per_plate_dna_qpcr > min_num - assay.controls.count():
          raise ValidationError(
            message=f"Minimum samples (qPCR - DNA) per plate cannot exceed {min_num - assay.controls.count()}"
          )
        
    if len(qpcr_rna_assays) > 0 and qpcr_plate:
      plates = []
      for p in qpcr_plate.all().order_by('size'):
        plates.append(p.size)
      min_num = plates[0]

      for assay in qpcr_rna_assays:
        if min_samples_per_plate_rna_qpcr > min_num - assay.controls.count():
          raise ValidationError(
            message=f"Minimum samples (qPCR - RNA) per plate cannot exceed {min_num - assay.controls.count()}"
          )
    # **VALIDATE qPCR PLATE MIN NUM** #
        
    # **VALIDATE PCR PLATE MIN NUM** #
    if len(pcr_dna_assays) > 0 and pcr_plate:
      plates = []
      for p in pcr_plate.all().order_by('size'):
        plates.append(p.size)
      min_num = plates[0]

      for assay in pcr_dna_assays:
        if min_samples_per_plate_dna_pcr > min_num - assay.controls.count():
          raise ValidationError(
            message=f"Minimum samples (PCR - DNA) per plate cannot exceed {min_num - assay.controls.count()}"
          )
        
    if len(pcr_rna_assays) > 0 and pcr_plate:
      plates = []
      for p in pcr_plate.all().order_by('size'):
        plates.append(p.size)
      min_num = plates[0]

      for assay in pcr_rna_assays:
        if min_samples_per_plate_rna_pcr > min_num - assay.controls.count():
          raise ValidationError(
            message=f"Minimum samples (PCR - RNA) per plate cannot exceed {min_num - assay.controls.count()}"
          )
    # **VALIDATE PCR PLATE MIN NUM** #
    
    # **VALIDATE PCR GEL MIN NUM** #
    if len(pcr_dna_assays) > 0 and gel or len(pcr_rna_assays) > 0 and gel:
      gels = []
      for g in gel.all().order_by('size'):
        gels.append(g.size)
      min_num = gels[0]

      for assay in pcr_dna_assays:
        if min_samples_per_gel > min_num - assay.controls.count():
          raise ValidationError(
            message=f"Minimum samples per gel cannot exceed {min_num - assay.controls.count()}"
          )
        
      for assay in pcr_rna_assays:
        if min_samples_per_gel > min_num - assay.controls.count():
          raise ValidationError(
            message=f"Minimum samples per gel cannot exceed {min_num - assay.controls.count()}"
          )
    # **VALIDATE PCR GEL MIN NUM** #
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['pcr_dna_protocol'].queryset = ThermalCyclerProtocol.objects.filter(user=self.user, type=ThermalCyclerProtocol.Types.DNA)
    self.fields['pcr_rna_protocol'].queryset = ThermalCyclerProtocol.objects.filter(user=self.user, type=ThermalCyclerProtocol.Types.RNA)
    self.fields['qpcr_dna_protocol'].queryset = ThermalCyclerProtocol.objects.filter(user=self.user, type=ThermalCyclerProtocol.Types.DNA)
    self.fields['qpcr_rna_protocol'].queryset = ThermalCyclerProtocol.objects.filter(user=self.user, type=ThermalCyclerProtocol.Types.RNA)

    self.fields['qpcr_plate'].queryset = Plate.objects.filter(user=self.user, type=Plate.Types.qPCR)
    self.fields['pcr_plate'].queryset = Plate.objects.filter(user=self.user, type=Plate.Types.PCR)
    self.fields['gel'].queryset = Gel.objects.filter(user=self.user)

    self.fields['name'].widget.attrs['class'] = 'form-control'

    self.fields['pcr_dna_protocol'].widget.attrs['class'] = 'form-select'
    self.fields['pcr_rna_protocol'].widget.attrs['class'] = 'form-select'
    self.fields['qpcr_dna_protocol'].widget.attrs['class'] = 'form-select'
    self.fields['qpcr_rna_protocol'].widget.attrs['class'] = 'form-select'

    self.fields['loading_method_dna'].widget.attrs['class'] = 'form-select'
    self.fields['loading_method_rna'].widget.attrs['class'] = 'form-select'
    self.fields['loading_method_qdna'].widget.attrs['class'] = 'form-select'
    self.fields['loading_method_qrna'].widget.attrs['class'] = 'form-select'

    self.fields['min_samples_per_plate_dna_qpcr'].widget.attrs['class'] = 'form-control'
    self.fields['min_samples_per_plate_rna_qpcr'].widget.attrs['class'] = 'form-control'
    self.fields['min_samples_per_plate_dna_pcr'].widget.attrs['class'] = 'form-control'
    self.fields['min_samples_per_plate_rna_pcr'].widget.attrs['class'] = 'form-control'
    self.fields['min_samples_per_gel'].widget.attrs['class'] = 'form-control'

    self.fields['min_samples_per_plate_dna_qpcr'].widget.attrs['min'] = 0
    self.fields['min_samples_per_plate_rna_qpcr'].widget.attrs['min'] = 0
    self.fields['min_samples_per_plate_dna_pcr'].widget.attrs['min'] = 0
    self.fields['min_samples_per_plate_rna_pcr'].widget.attrs['min'] = 0
    self.fields['min_samples_per_gel'].widget.attrs['min'] = 0

    self.fields['min_samples_per_plate_dna_qpcr'].required = False
    self.fields['min_samples_per_plate_rna_qpcr'].required = False
    self.fields['min_samples_per_plate_dna_pcr'].required = False
    self.fields['min_samples_per_plate_rna_pcr'].required = False

    self.fields['loading_method_dna'].required = False
    self.fields['loading_method_rna'].required = False
    self.fields['loading_method_qdna'].required = False
    self.fields['loading_method_qrna'].required = False

    self.fields['min_samples_per_gel'].required = False

    if self.instance.is_dna_pcr:
      self.fields['min_samples_per_plate_dna_pcr'].required = True
      self.fields['loading_method_dna'].required = True
      self.fields['min_samples_per_gel'].required = True

    if self.instance.is_rna_pcr:
      self.fields['min_samples_per_plate_rna_pcr'].required = True
      self.fields['loading_method_rna'].required = True
      self.fields['min_samples_per_gel'].required = True

    if self.instance.is_dna_qpcr:
      self.fields['min_samples_per_plate_dna_qpcr'].required = True
      self.fields['loading_method_qdna'].required = True

    if self.instance.is_rna_qpcr:
      self.fields['min_samples_per_plate_rna_qpcr'].required = True
      self.fields['loading_method_qrna'].required = True

  class Meta:
    model = Process
    exclude = ['user', 'samples', 'is_processed', 'date_processed', 'pcr_dna_json', 'pcr_rna_json', 'qpcr_dna_json', 'qpcr_rna_json', 'batches']