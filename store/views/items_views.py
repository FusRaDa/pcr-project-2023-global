from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from ..models.items import Kit, StorePlate, StoreReagent, StoreTube
from ..forms.items import KitForm


@staff_member_required(login_url='login')
def create_kit(request):

  form = KitForm()
  
  context = {'form': form}
  return render(request, 'items/create_kit.html', context)