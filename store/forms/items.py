from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from ..models.items import Kit, StorePlate, StoreTube, StoreReagent


class KitForm(ModelForm):

  class Meta:
    model = Kit
    fields = '__all__'


class StorePlateForm(ModelForm):

  class Meta:
    model = StorePlate
    exclude = ['kit']


class StoreTubeForm(ModelForm):

  class Meta:
    model = StoreTube
    exclude = ['kit']


class StoreReagentForm(ModelForm):

  class Meta:
    model = StoreReagent
    exclude = ['kit']