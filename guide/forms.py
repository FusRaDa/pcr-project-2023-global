from django.forms import ModelForm
from django import forms

from store.models.affiliates import Contact

class ContactForm(ModelForm):

  class Meta:
    model = Contact
    fields = '__all__'