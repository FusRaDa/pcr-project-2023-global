from django.forms import ModelForm
from django import forms

from store.models.affiliates import Contact

class ContactForm(ModelForm):

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super().__init__(*args, **kwargs) 
 
    self.fields['brand'].widget.attrs['class'] = 'form-control'
    self.fields['company'].widget.attrs['class'] = 'form-control'
    self.fields['first_name'].widget.attrs['class'] = 'form-control'
    self.fields['last_name'].widget.attrs['class'] = 'form-control'
    self.fields['email'].widget.attrs['class'] = 'form-control'
    self.fields['phone_number'].widget.attrs['class'] = 'form-control'

  class Meta:
    model = Contact
    fields = '__all__'