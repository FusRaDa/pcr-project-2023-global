from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.contrib import messages
from users.models import User

from ..models.pcr import ThermalCyclerProtocol, Process, ProcessPlate

@login_required(login_url='login')
def tcprotocols(request):
  protocols = ThermalCyclerProtocol.objects.filter(user=request.user)
  context = {'protocols': protocols}
  return render(request, 'pcr/tcprotocols.html', context)