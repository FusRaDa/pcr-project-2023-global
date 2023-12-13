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

  class Meta:
    model = Contact
    fields = '__all__'
    exclude = ['brand']