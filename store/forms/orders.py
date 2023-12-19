from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from ..models.orders import Order, KitOrder
from pcr.models.inventory import Plate, Tube, Reagent


class KitOrderForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['amount_ordered'].widget.attrs['class'] = 'form-control'
    self.fields['amount_ordered'].initial = self.instance

  class Meta:
    model = KitOrder
    exclude = ['order', 'kit']