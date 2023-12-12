from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from ..models.orders import Order, KitOrder


class KitOrderForm(ModelForm):

  class Meta:
    model = KitOrder
    fields = '__all__'