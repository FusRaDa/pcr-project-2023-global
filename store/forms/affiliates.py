from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from ..models.affiliates import Brand, Contact

class BrandForm(ModelForm):

  class Meta:
    model = Brand
    fields = '__all__'


class ContactForm(ModelForm):

  class Meta:
    model = Contact
    fields = '__all__'
    exclude = ['brand']