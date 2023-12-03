from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.assay import Assay, AssayCode, ReagentAssay, Fluorescence, Control
from ..models.inventory import Reagent, Location


class FluorescenceForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) 
    self.fields['name'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Fluorescence
    exclude = ['user']


class ControlForm(ModelForm):

  location = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)
  
  exp_date = forms.DateField(
      widget=forms.DateInput(attrs={'type': 'date'}),
      label='Date Start',
      required=False)

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
    required=True)
  
  controls = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)
  
  reagents = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=True)
  
  def clean(self):
    cleaned_data = super().clean()
    reaction_volume = cleaned_data.get('reaction_volume')
    sample_volume = cleaned_data.get('sample_volume')
    controls = cleaned_data.get('controls')
    reagents = cleaned_data.get('reagents')

    if reaction_volume < sample_volume:
      raise ValidationError(
        message="Reaction volume must be greater or equal to the sample volume."
      )
    
    neg_ctrl_found = 0
    for control in controls:
      if control.is_negative_ctrl == True:
        neg_ctrl_found += 1

    if neg_ctrl_found != 1:
      raise ValidationError(
        message="Assay must contain one negative control."
      )
    
    water_reagent_found = 0
    for reagent in reagents:
      if reagent.pcr_reagent == Reagent.PCRReagent.WATER:
        water_reagent_found += 1
    
    if water_reagent_found != 1:
      raise ValidationError(
        message="Assay must contain one reagent as PCR water"
      )

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['fluorescence'].queryset = Fluorescence.objects.filter(user=self.user)
    self.fields['controls'].queryset = Control.objects.filter(user=self.user)
    self.fields['reagents'].queryset = Reagent.objects.filter(user=self.user, usage=Reagent.Usages.PCR)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['method'].widget.attrs['class'] = 'form-select'
    self.fields['type'].widget.attrs['class'] = 'form-select'
    self.fields['sample_volume'].widget.attrs['class'] = 'form-control'
    self.fields['reaction_volume'].widget.attrs['class'] = 'form-control'
    
  class Meta:
    model = Assay
    exclude = ['user']


class ReagentAssayForm(ModelForm):

  def clean(self):
    cleaned_data = super().clean()
    final_concentration = cleaned_data.get('final_concentration')
    final_concentration_unit = cleaned_data.get('final_concentration_unit')

    if self.instance.reagent.pcr_reagent != Reagent.PCRReagent.WATER.name and (final_concentration == None or final_concentration_unit == None):
      raise ValidationError(
        message="Reagents that are not water must have a final concentration."
      )
    
    if self.instance.reagent.pcr_reagent == Reagent.PCRReagent.WATER.name and (final_concentration != None or final_concentration_unit != None):
      raise ValidationError (
        message="Water reagent's final concentration and unit must be left empty."
      )
    
    if self.instance.reagent.pcr_reagent == Reagent.PCRReagent.POLYMERASE.name and final_concentration_unit != Reagent.ConcentrationUnits.UNITS.name:
      raise ValidationError(
        message="Polymerase must have the concentration unit of U/\u00B5L."
      )
    
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    if self.instance.reagent.pcr_reagent == Reagent.PCRReagent.WATER:
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
    pcr_dna = cleaned_data.get('pcr_dna')
    pcr_rna = cleaned_data.get('pcr_rna')
    qpcr_dna = cleaned_data.get('qpcr_dna')
    qpcr_rna = cleaned_data.get('qpcr_rna')

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