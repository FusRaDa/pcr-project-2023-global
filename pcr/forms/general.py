from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.assay import AssayCode
from ..models.batch import ExtractionProtocol
from ..models.inventory import Location, Plate, Gel, Reagent


class SearchTubeForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

class SearchLadderForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)


class SearchPlateForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  CHOICES = [Plate.Sizes.choices, ('', '------')]
  size = forms.ChoiceField(choices=CHOICES, required=False)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)


class SearchGelForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  CHOICES = [(None, '------'), Gel.Sizes.choices]
  size = forms.ChoiceField(choices=CHOICES, required=False)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)


class SearchReagentForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  usage = forms.ChoiceField(choices=Reagent.Usages.choices)

  CHOICES = [(None, '------'), Reagent.PCRReagent.choices]
  pcr_reagent = forms.ChoiceField(choices=CHOICES)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)


class SearchBatchForm(forms.Form):
  name = forms.CharField(max_length=100, required=False)
  lab_id = forms.CharField(max_length=4, required=False)

  panel = forms.ModelChoiceField(queryset=None, required=False)
  extraction_protocol = forms.ModelChoiceField(queryset=None, required=False)

  start_date = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  end_date = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date End',
    required=False)
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['panel'].queryset = AssayCode.objects.filter(user=self.user)
    self.fields['extraction_protocol'].queryset = ExtractionProtocol.objects.filter(user=self.user)

    self.fields['panel'].widget.attrs['class'] = 'form-select'
    self.fields['extraction_protocol'].widget.attrs['class'] = 'form-select'
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['lab_id'].widget.attrs['class'] = 'form-control'
    self.fields['start_date'].widget.attrs['class'] = 'form-control'
    self.fields['end_date'].widget.attrs['class'] = 'form-control'


class SearchProcessForm(forms.Form):
  name = forms.CharField(max_length=100, required=False)

  panel = forms.ModelChoiceField(queryset=None, required=False)

  lab_id = forms.CharField(max_length=4, required=False)

  start_date = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date Start',
    required=False)
  
  end_date = forms.DateTimeField(
    widget=forms.DateInput(attrs={'type': 'date'}),
    label='Date End',
    required=False)

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['panel'].queryset = AssayCode.objects.filter(user=self.user)

    self.fields['panel'].widget.attrs['class'] = 'form-select'
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['lab_id'].widget.attrs['class'] = 'form-control'
    self.fields['start_date'].widget.attrs['class'] = 'form-control'
    self.fields['end_date'].widget.attrs['class'] = 'form-control'


class DeletionForm(forms.Form):
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
        message="Invalid value entered, please try again."
      )