from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *


class CreateBatchForm(ModelForm):
  class Meta:
    model = Batch
    exclude = ["user"]

