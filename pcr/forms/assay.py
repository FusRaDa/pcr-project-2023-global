from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.assay import Assay, AssayCode, ReagentAssay, Fluorescence, Control, ControlAssay
from ..models.inventory import Reagent, Location
from ..custom.constants import LIMITS


class FluorescenceForm(ModelForm):

  def clean(self):
    cleaned_data = super().clean()
    name = cleaned_data.get('name')

    name_exists = Fluorescence.objects.filter(user=self.user, name=name).exists()
    if name_exists:
      raise ValidationError(
        message=f"Fluorescence with the name: {name} already exists."
      )
    
    if Fluorescence.objects.filter(user=self.user).count() >= LIMITS.MAX_FLUORESCENCE_LIMIT:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_FLUORESCENCE_LIMIT} fluorescence tags. Should you require more, please contact us!"
      )

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['name'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Fluorescence
    exclude = ['user']


class ControlForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  exp_date = forms.DateField(
      widget=forms.DateInput(attrs={'type': 'date'}),
      label='Date Start',
      required=False)
  
  def clean(self):
    cleaned_data = super().clean()
    lot_number = cleaned_data.get('lot_number')

    lot_number_exists = Control.objects.filter(user=self.user, lot_number=lot_number).exists()
    if lot_number_exists:
      raise ValidationError(
        message=f"A control with the lot number: {lot_number} already exists."
      )

    if not self.user.is_subscribed:
      if Control.objects.filter(user=self.user).count() >= LIMITS.CONTROL_LIMIT:
        raise ValidationError(
          message=f"You have reached the maximum number of {LIMITS.CONTROL_LIMIT} controls. Consider upgrading or deleting your controls."
        )
      
    if Control.objects.filter(user=self.user).count() >= LIMITS.MAX_CONTROL_LIMIT:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_CONTROL_LIMIT} controls. Should you require more, please contact us!"
      )
 
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['lot_number'].widget.attrs['class'] = 'form-control'
    self.fields['amount'].widget.attrs['class'] = 'form-control'
    self.fields['exp_date'].widget.attrs['class'] = 'form-control'
    
  class Meta:
    model = Control
    exclude = ['user']
 

class AssayForm(ModelForm):

  fluorescence = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False)
  
  def clean(self):
    cleaned_data = super().clean()
    name = cleaned_data.get('name')
    reaction_volume = cleaned_data.get('reaction_volume')
    sample_volume = cleaned_data.get('sample_volume')
    fluorescence = cleaned_data.get('fluorescence')
    method = cleaned_data.get('method')

    ladder = cleaned_data.get('ladder')
    ladder_volume_per_gel = cleaned_data.get('ladder_volume_per_gel')

    dye = cleaned_data.get('dye')
    dye_volume_per_well = cleaned_data.get('dye_volume_per_well')
    dye_in_ladder = cleaned_data.get('dye_in_ladder')

    name_exists = Assay.objects.filter(user=self.user, name=name).exists()
    if name_exists:
      raise ValidationError(
        message=f"Assay with the name: {name} already exists."
      )

    if not self.user.is_subscribed:
      if Assay.objects.filter(user=self.user).count() >= LIMITS.ASSAY_LIMIT:
        raise ValidationError(
          message=f"You have reached the maximum number of {LIMITS.ASSAY_LIMIT} assays. Consider upgrading or deleting your assays."
        )
      
    if Assay.objects.filter(user=self.user).count() >= LIMITS.MAX_ASSAY_LIMIT:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_ASSAY_LIMIT} assays. Should you require more, please contact us!"
      )

    if ladder == None and method == Assay.Methods.PCR:
      raise ValidationError(
        message="PCR assays must contain a ladder."
      )
    
    if ladder != None and method == Assay.Methods.qPCR:
      raise ValidationError(
        message="qPCR assays do not require a ladder."
      )
    
    if ladder_volume_per_gel == 0 and method == Assay.Methods.PCR:
      raise ValidationError(
        message="PCR assays must contain a ladder volume per gel."
      )
    
    if ladder_volume_per_gel > 0 and method == Assay.Methods.qPCR:
      raise ValidationError(
        message="qPCR assays do not require a ladder volume per gel."
      )
    
    if dye == None and method == Assay.Methods.PCR:
      raise ValidationError(
        message="PCR assays must contain a loading gel dye."
      )
    
    if dye != None and method == Assay.Methods.qPCR:
      raise ValidationError(
        message="qPCR assays do not require a loading gel dye."
      )
    
    if dye_volume_per_well == 0 and method == Assay.Methods.PCR:
      raise ValidationError(
        message="PCR assays must contain a loading gel dye volume per well."
      )
    
    if dye_volume_per_well > 0 and method == Assay.Methods.qPCR:
      raise ValidationError(
        message="qPCR assays do not require a loading gel dye volume per well."
      )
    
    if dye_in_ladder == True and method == Assay.Methods.qPCR:
      raise ValidationError(
        message="qPCR assays do not require a loading gel dye."
      )

    if method == Assay.Methods.qPCR and not fluorescence:
      raise ValidationError(
        message="qPCR assays require fluorescense."
      )
    
    if method == Assay.Methods.PCR and fluorescence:
      raise ValidationError(
        message="PCR assays do not require fluorescense."
      )

    if reaction_volume < sample_volume:
      raise ValidationError(
        message="Reaction volume must be greater or equal to the sample volume."
      )
    
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['fluorescence'].queryset = Fluorescence.objects.filter(user=self.user)
 
    self.fields['fluorescence'].error_messages = {'required': "Assay requires at least one fluorescence"}
 
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['method'].widget.attrs['class'] = 'form-select'
    self.fields['type'].widget.attrs['class'] = 'form-select'
    self.fields['sample_volume'].widget.attrs['class'] = 'form-control'
    self.fields['reaction_volume'].widget.attrs['class'] = 'form-control'
    self.fields['ladder'].widget.attrs['class'] = 'form-select'
    self.fields['ladder_volume_per_gel'].widget.attrs['class'] = 'form-control'
    self.fields['dye'].widget.attrs['class'] = 'form-select'
    self.fields['dye_volume_per_well'].widget.attrs['class'] = 'form-control'
    self.fields['multiplicates'].widget.attrs['class'] = 'form-control'
    
  class Meta:
    model = Assay
    exclude = ['user', 'controls', 'reagents']


class ControlAssayForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['order'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = ControlAssay
    exclude = ['control', 'assay']


class ReagentAssayForm(ModelForm):

  def clean(self):
    cleaned_data = super().clean()
    final_concentration = cleaned_data.get('final_concentration')
    final_concentration_unit = cleaned_data.get('final_concentration_unit')

    if self.instance.reagent.pcr_reagent != Reagent.PCRReagent.WATER.name and final_concentration == None:
      raise ValidationError(
        message=f"Reagents ({self.instance.reagent.name}) that are not water must have a final concentration."
      )
    
    if self.instance.reagent.pcr_reagent == Reagent.PCRReagent.WATER.name and final_concentration != None or self.instance.reagent.pcr_reagent == Reagent.PCRReagent.WATER.name and final_concentration_unit != None:
      raise ValidationError (
        message="Water reagent's final concentration and unit must be left empty."
      )
 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['final_concentration'].widget.attrs['class'] = 'form-control'
    self.fields['final_concentration_unit'].widget.attrs['class'] = 'form-select'
    self.fields['order'].widget.attrs['class'] = 'form-control'

    self.fields['final_concentration_unit'].initial = self.instance.final_concentration_unit

    if self.instance.reagent.pcr_reagent == Reagent.PCRReagent.WATER.name:
      self.fields['final_concentration'].widget.attrs['disabled'] = 'True'
      self.fields['final_concentration_unit'].widget.attrs['disabled'] = 'True'
    
  class Meta:
    model = ReagentAssay
    exclude = ['reagent', 'assay']


class AssayCodeForm(ModelForm):

  pcr_dna = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False,)
  
  pcr_rna = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False,)
  
  qpcr_dna = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False,)
  
  qpcr_rna = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False,)
  
  def clean(self):
    cleaned_data = super().clean()
    name = cleaned_data.get('name')
    pcr_dna = cleaned_data.get('pcr_dna')
    pcr_rna = cleaned_data.get('pcr_rna')
    qpcr_dna = cleaned_data.get('qpcr_dna')
    qpcr_rna = cleaned_data.get('qpcr_rna')

    name_exists = AssayCode.objects.filter(user=self.user, name=name).exists()
    if name_exists:
      raise ValidationError(
        message=f"Panel with the name: {name} already exists."
      )

    if not self.user.is_subscribed:
      if AssayCode.objects.filter(user=self.user).count() >= LIMITS.ASSAY_CODE_LIMIT:
        raise ValidationError(
          message=f"You have reached the maximum number of {LIMITS.ASSAY_CODE_LIMIT} panels. Consider upgrading or deleting your panels."
        )
      
    if AssayCode.objects.filter(user=self.user).count() >= LIMITS.MAX_ASSAY_CODE_LIMIT:
      raise ValidationError(
        message=f"You have reached the maximum number of {LIMITS.MAX_ASSAY_CODE_LIMIT} panels. Should you require more, please contact us!"
      )

    for assay in pcr_dna | pcr_rna | qpcr_dna | qpcr_rna:
      if not assay.is_complete:
        raise ValidationError(
          message=f"{assay} is incomplete, you cannot select this assay."
        )

    if not pcr_dna and not pcr_rna and not qpcr_dna and not qpcr_rna:
      raise ValidationError(
        message="Please select at least one assay for this panel."
      )
    
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs)
    self.fields['pcr_dna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.DNA, method=Assay.Methods.PCR).order_by('name')
    self.fields['pcr_rna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.RNA, method=Assay.Methods.PCR).order_by('name')
    self.fields['qpcr_dna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.DNA, method=Assay.Methods.qPCR).order_by('name')
    self.fields['qpcr_rna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.RNA, method=Assay.Methods.qPCR).order_by('name')
    self.fields['name'].widget.attrs['class'] = 'form-control'

    try:
      self.fields['pcr_dna'].initial = self.instance.assays.all()
      self.fields['pcr_rna'].initial = self.instance.assays.all()
      self.fields['qpcr_dna'].initial = self.instance.assays.all()
      self.fields['qpcr_rna'].initial = self.instance.assays.all()
    except ValueError:
      pass

  class Meta:
    model = AssayCode
    exclude = ['user', 'assays']