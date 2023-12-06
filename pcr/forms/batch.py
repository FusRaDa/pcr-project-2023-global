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
    required=False)
  
  extraction_protocol_dna = forms.ModelChoiceField(
    queryset=None,
    widget=forms.RadioSelect(attrs={'class': 'radio-ext-prot'}),
    required=False,)
  
  extraction_protocol_rna = forms.ModelChoiceField(
    queryset=None,
    widget=forms.RadioSelect(attrs={'class': 'radio-ext-prot'}),
    required=False)

  extraction_protocol_tn = forms.ModelChoiceField(
    queryset=None,
    widget=forms.RadioSelect(attrs={'class': 'radio-ext-prot'}),
    required=False)
  
  def clean(self):
    cleaned_data = super().clean()
    lab_id = cleaned_data.get('lab_id')
    code = cleaned_data.get('code')
    extraction_protocol_dna = cleaned_data.get('extraction_protocol_dna')
    extraction_protocol_rna = cleaned_data.get('extraction_protocol_rna')
    extraction_protocol_tn = cleaned_data.get('extraction_protocol_tn')

    if Batch.objects.filter(user=self.user, lab_id=lab_id).exists():
      raise ValidationError(
        message="A batch with this Lab ID already exists."
      )

    if extraction_protocol_dna == None and extraction_protocol_rna == None and extraction_protocol_tn == None:
      raise ValidationError(
        message="Please select an extraction protocol."
      )
    
    if extraction_protocol_dna != None and (extraction_protocol_rna !=None or extraction_protocol_tn != None):
      raise ValidationError(
        message="Only one extraction protocol can be selected. Reset radios and select again."
      )
    
    if extraction_protocol_rna != None and (extraction_protocol_dna !=None or extraction_protocol_tn != None):
      raise ValidationError(
        message="Only one extraction protocol can be selected. Reset radios and select again."
      )
    
    if extraction_protocol_tn != None and (extraction_protocol_rna !=None or extraction_protocol_dna != None):
      raise ValidationError(
        message="Only one extraction protocol can be selected. Reset radios and select again."
      )
    
    if code == None:
      raise ValidationError(
        message="Please select a panel."
      )
    
    if extraction_protocol_dna != None:
      for assay in code.assays.all():
        if assay.type != Assay.Types.DNA:
          raise ValidationError(
            message=f"Assay: {assay.name} with type {assay.type} is not compatible with {extraction_protocol_dna}."
          )
        
    if extraction_protocol_rna != None:
      for assay in code.assays.all():
        if assay.type != Assay.Types.RNA:
          raise ValidationError(
            message=f"Assay: {assay.name} with type {assay.type} is not compatible with {extraction_protocol_rna}."
          )
    
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
    exclude = ['user', 'date_performed', 'extraction_protocol']


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

  pcr_dna = forms.ModelMultipleChoiceField(
    queryset=Assay.objects.none(),
    widget=forms.CheckboxSelectMultiple,
    required=False,)
  
  pcr_rna = forms.ModelMultipleChoiceField(
    queryset=Assay.objects.none(),
    widget=forms.CheckboxSelectMultiple,
    required=False,)
  
  qpcr_dna = forms.ModelMultipleChoiceField(
    queryset=Assay.objects.none(),
    widget=forms.CheckboxSelectMultiple,
    required=False,)
  
  qpcr_rna = forms.ModelMultipleChoiceField(
    queryset=Assay.objects.none(),
    widget=forms.CheckboxSelectMultiple,
    required=False,)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 

    try:
      self.fields['pcr_dna'].initial = self.instance.assays.all()
      self.fields['pcr_rna'].initial = self.instance.assays.all()
      self.fields['qpcr_dna'].initial = self.instance.assays.all()
      self.fields['qpcr_rna'].initial = self.instance.assays.all()
    except ValueError:
      pass

    if self.instance.batch.extraction_protocol.type == ExtractionProtocol.Types.TOTAL_NUCLEIC:
      self.fields['pcr_dna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.DNA, method=Assay.Methods.PCR).order_by('name')
      self.fields['pcr_rna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.RNA, method=Assay.Methods.PCR).order_by('name')
      self.fields['qpcr_dna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.DNA, method=Assay.Methods.qPCR).order_by('name')
      self.fields['qpcr_rna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.RNA, method=Assay.Methods.qPCR).order_by('name')

    if self.instance.batch.extraction_protocol.type == ExtractionProtocol.Types.DNA: 
      self.fields['pcr_dna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.DNA, method=Assay.Methods.PCR).order_by('name')
      self.fields['qpcr_dna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.DNA, method=Assay.Methods.qPCR).order_by('name')

    if self.instance.batch.extraction_protocol.type == ExtractionProtocol.Types.RNA:
      self.fields['pcr_rna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.RNA, method=Assay.Methods.PCR).order_by('name')
      self.fields['qpcr_rna'].queryset = Assay.objects.filter(user=self.user, type=Assay.Types.RNA, method=Assay.Methods.qPCR).order_by('name')

  class Meta:
    model = Sample
    exclude = ['user', 'lab_id_num', 'sample_id', 'assays', 'batch']