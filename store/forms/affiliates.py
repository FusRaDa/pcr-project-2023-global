from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from ..models.affiliates import Brand, Contact

class BrandForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['logo'].widget.attrs['class'] = 'form-control'
    self.fields['is_affiliated'].widget.attrs['class'] = 'form-check-input'

  class Meta:
    model = Brand
    fields = '__all__'


class ContactForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['company'].widget.attrs['class'] = 'form-control'
    self.fields['first_name'].widget.attrs['class'] = 'form-control'
    self.fields['last_name'].widget.attrs['class'] = 'form-control'
    self.fields['email'].widget.attrs['class'] = 'form-control'
    self.fields['phone_number'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Contact
    exclude = ['brand']


class BrandContactForm(ModelForm):

  brand = forms.ModelChoiceField(
    queryset=Brand.objects.all(),
    widget=forms.RadioSelect,
    required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['company'].widget.attrs['class'] = 'form-control'
    self.fields['first_name'].widget.attrs['class'] = 'form-control'
    self.fields['last_name'].widget.attrs['class'] = 'form-control'
    self.fields['email'].widget.attrs['class'] = 'form-control'
    self.fields['phone_number'].widget.attrs['class'] = 'form-control'

    self.fields['company'].widget.attrs['readonly'] = 'True'
    self.fields['first_name'].widget.attrs['readonly'] = 'True'
    self.fields['last_name'].widget.attrs['readonly'] = 'True'
    self.fields['email'].widget.attrs['readonly'] = 'True'
    self.fields['phone_number'].widget.attrs['readonly'] = 'True'

  class Meta:
    model = Contact
    fields = '__all__'

