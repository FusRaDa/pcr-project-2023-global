from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.assay import AssayCode, Assay
from ..models.batch import ExtractionProtocol
from ..models.inventory import Location, Plate, Gel, Reagent


class SearchExtractionProtocolForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)

  TYPE_CHOICES = [(None, "------"), (ExtractionProtocol.Types.DNA, "DNA"), (ExtractionProtocol.Types.RNA, "RNA"), (ExtractionProtocol.Types.TOTAL_NUCLEIC, "Total-nucleic")]
  type = forms.ChoiceField(choices=TYPE_CHOICES, required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['text_search'].widget.attrs['class'] = 'form-control'
    self.fields['type'].widget.attrs['class'] = 'form-select'


class SearchAssayCodeForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['text_search'].widget.attrs['class'] = 'form-control'


class SearchFluorescenseForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['text_search'].widget.attrs['class'] = 'form-control'


class SearchControlForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  SORT_CHOICES = [('exp_date', "Expiration Date ⮝"), ('threshold_diff', "Closest to Threshold ⮝"), ('-last_updated', "Last Updated ⮝"), ('last_updated', "Last Updated ⮟"), ('-date_created', "Date Created ⮝"), ('date_created', "Date Created ⮟")]
  sort = forms.ChoiceField(choices=SORT_CHOICES, required=True, initial=SORT_CHOICES[0])

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['location'].widget.attrs['class'] = 'form-select'
    self.fields['text_search'].widget.attrs['class'] = 'form-control'
    self.fields['sort'].widget.attrs['class'] = 'form-select'


class SearchAssayForm(forms.Form):
  name = forms.CharField(max_length=100, required=False)

  METHOD_CHOICES = [(None, "------"), (Assay.Methods.PCR, "PCR"), (Assay.Methods.qPCR, "qPCR")]
  method = forms.ChoiceField(choices=METHOD_CHOICES, required=False)

  TYPE_CHOICES = [(None, "------"), (Assay.Types.DNA, "DNA"), (Assay.Types.RNA, "RNA")]
  type = forms.ChoiceField(choices=TYPE_CHOICES, required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) 
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['method'].widget.attrs['class'] = 'form-select'
    self.fields['type'].widget.attrs['class'] = 'form-select'


class SearchTubeForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  SORT_CHOICES = [('exp_date', "Expiration Date ⮝"), ('threshold_diff', "Closest to Threshold ⮝"), ('-last_updated', "Last Updated ⮝"), ('last_updated', "Last Updated ⮟"), ('-date_created', "Date Created ⮝"), ('date_created', "Date Created ⮟")]
  sort = forms.ChoiceField(choices=SORT_CHOICES, required=True, initial=SORT_CHOICES[0])

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['text_search'].widget.attrs['class'] = 'form-control'
    self.fields['location'].widget.attrs['class'] = 'form-select'
    self.fields['sort'].widget.attrs['class'] = 'form-select'



class SearchLadderForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  SORT_CHOICES = [('exp_date', "Expiration Date"), ('threshold_diff', "Closest to Threshold"), ('-last_updated', "Last Updated ⮝"), ('last_updated', "Last Updated ⮟"), ('-date_created', "Date Created ⮝"), ('date_created', "Date Created ⮟")]
  sort = forms.ChoiceField(choices=SORT_CHOICES, required=True, initial=SORT_CHOICES[0])

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['text_search'].widget.attrs['class'] = 'form-control'
    self.fields['location'].widget.attrs['class'] = 'form-select'
    self.fields['sort'].widget.attrs['class'] = 'form-select'


class SearchDyeForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  SORT_CHOICES = [('exp_date', "Expiration Date"), ('threshold_diff', "Closest to Threshold"), ('-last_updated', "Last Updated ⮝"), ('last_updated', "Last Updated ⮟"), ('-date_created', "Date Created ⮝"), ('date_created', "Date Created ⮟")]
  sort = forms.ChoiceField(choices=SORT_CHOICES, required=True, initial=SORT_CHOICES[0])

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['text_search'].widget.attrs['class'] = 'form-control'
    self.fields['location'].widget.attrs['class'] = 'form-select'
    self.fields['sort'].widget.attrs['class'] = 'form-select'


class SearchPlateForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  SIZE_CHOICES = [(None, '------'), (Plate.Sizes.EIGHT, '8'), (Plate.Sizes.TWENTY_FOUR, '24'), (Plate.Sizes.FOURTY_EIGHT, '48'), (Plate.Sizes.NINETY_SIX, '96'), (Plate.Sizes.THREE_HUNDRED_EIGHTY_FOUR, '384')]
  size = forms.ChoiceField(choices=SIZE_CHOICES, required=False)

  TYPE_CHOICES = [(None, '------'), (Plate.Types.PCR, 'PCR'), (Plate.Types.qPCR, 'qPCR')]
  type = forms.ChoiceField(choices=TYPE_CHOICES, required=False)

  SORT_CHOICES = [('exp_date', "Expiration Date"), ('threshold_diff', "Closest to Threshold"), ('-last_updated', "Last Updated ⮝"), ('last_updated', "Last Updated ⮟"), ('-date_created', "Date Created ⮝"), ('date_created', "Date Created ⮟")]
  sort = forms.ChoiceField(choices=SORT_CHOICES, required=True, initial=SORT_CHOICES[0])

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['text_search'].widget.attrs['class'] = 'form-control'
    self.fields['location'].widget.attrs['class'] = 'form-select'
    self.fields['size'].widget.attrs['class'] = 'form-select'
    self.fields['type'].widget.attrs['class'] = 'form-select'
    self.fields['sort'].widget.attrs['class'] = 'form-select'


class SearchGelForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  CHOICES = [(None, '------'), (Gel.Sizes.TWELVE, '12'), (Gel.Sizes.TWENTY_FOUR, '24'), (Gel.Sizes.FOURTY_EIGHT, '48')]
  size = forms.ChoiceField(choices=CHOICES, required=False)

  SORT_CHOICES = [('exp_date', "Expiration Date"), ('threshold_diff', "Closest to Threshold"), ('-last_updated', "Last Updated ⮝"), ('last_updated', "Last Updated ⮟"), ('-date_created', "Date Created ⮝"), ('date_created', "Date Created ⮟")]
  sort = forms.ChoiceField(choices=SORT_CHOICES, required=True, initial=SORT_CHOICES[0])

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['text_search'].widget.attrs['class'] = 'form-control'
    self.fields['location'].widget.attrs['class'] = 'form-select'
    self.fields['size'].widget.attrs['class'] = 'form-select'
    self.fields['sort'].widget.attrs['class'] = 'form-select'


class SearchReagentForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)
  location = forms.ModelChoiceField(queryset=None, required=False)

  USAGE_CHOICES = [(None, '------'), (Reagent.Usages.EXTRACTION, 'EXTRACTION'), (Reagent.Usages.PCR, 'PCR')]
  usage = forms.ChoiceField(choices=USAGE_CHOICES, required=False)

  PCR_REAGENT_CHOICES = [(None, '------'), (Reagent.PCRReagent.GENERAL, 'General'), (Reagent.PCRReagent.PRIMER, 'Primer'), (Reagent.PCRReagent.POLYMERASE, 'Polymerase'), (Reagent.PCRReagent.MIXTURE, 'Mixture'), (Reagent.PCRReagent.WATER, 'Water')]
  pcr_reagent = forms.ChoiceField(choices=PCR_REAGENT_CHOICES, required=False)

  SORT_CHOICES = [('exp_date', "Expiration Date"), ('threshold_diff', "Closest to Threshold"), ('-last_updated', "Last Updated ⮝"), ('last_updated', "Last Updated ⮟"), ('-date_created', "Date Created ⮝"), ('date_created', "Date Created ⮟")]
  sort = forms.ChoiceField(choices=SORT_CHOICES, required=True, initial=SORT_CHOICES[0])

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
    self.fields['location'].queryset = Location.objects.filter(user=self.user)

    self.fields['text_search'].widget.attrs['class'] = 'form-control'
    self.fields['usage'].widget.attrs['class'] = 'form-select'
    self.fields['location'].widget.attrs['class'] = 'form-select'
    self.fields['pcr_reagent'].widget.attrs['class'] = 'form-select'
    self.fields['sort'].widget.attrs['class'] = 'form-select'


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


class TextSearchForm(forms.Form):
  text_search = forms.CharField(max_length=100, required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs) 
    self.fields['text_search'].widget.attrs['class'] = 'form-control'


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