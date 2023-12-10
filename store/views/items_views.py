from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from ..models.items import Kit, StorePlate, StoreReagent, StoreTube


@staff_member_required(redirect_field_name='batches')
def create_kit(request):
  print('kit')