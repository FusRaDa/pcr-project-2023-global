from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.http import HttpResponse
from django.contrib import messages
from users.models import User

from ..forms.general import DeletionForm
from ..forms.pcr import ThermalCyclerProtocolForm
from ..models.pcr import ThermalCyclerProtocol, Process, ProcessPlate
from ..models.batch import Batch, Sample


@login_required(login_url='login')
def extracted_batches(request):
  batches = Batch.objects.filter(user=request.user, is_extracted=True).order_by('-date_created')

  process = Process.objects.filter(user=request.user, is_processed=False)
  if not process.exists():
    process = Process.objects.create(user=request.user)
  else:
    process = Process.objects.get(user=request.user, is_processed=False)

  context = {'batches': batches, 'process': process}
  return render(request, 'pcr/extracted_batches.html', context)


@login_required(login_url='login')
def add_batch_samples(request, username, process_pk, batch_pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no sample or process found.")
    return redirect('extracted_batches')
  
  try:
    batch = Batch.objects.get(user=user, pk=batch_pk)
    process = Process.objects.get(user=request.user, pk=process_pk, is_processed=False)
  except ObjectDoesNotExist:
    messages.error(request, "There is no sample or process found.")
    return redirect('extracted_batches')
  
  if 'all' in request.POST:
    for sample in batch.sample_set.all():
      process.samples.add(sample)
      context = {'sample': sample, 'process': process}
      return render(request, 'pcr/samples_in_process.html', context) 

  return HttpResponse(status=200)


@login_required(login_url='login')
def add_sample_to_process(request, username, process_pk, sample_pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no sample or process found.")
    return redirect('extracted_batches')
  
  try:
    sample = Sample.objects.get(user=user, pk=sample_pk)
    process = Process.objects.get(user=request.user, pk=process_pk, is_processed=False)
  except ObjectDoesNotExist:
    messages.error(request, "There is no sample or process found.")
    return redirect('extracted_batches')
  
  if 'add' in request.POST:
    if not process.samples.contains(sample):
      process.samples.add(sample)
      context = {'sample': sample, 'process': process}
      return render(request, 'pcr/samples_in_process.html', context)

  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_sample_from_process(request, username, process_pk, sample_pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no sample or process found.")
    return redirect('extracted_batches')
  
  try:
    sample = Sample.objects.get(user=user, pk=sample_pk)
    process = Process.objects.get(user=request.user, is_processed=False, pk=process_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no sample or process found.")
    return redirect('extracted_batches')
  
  if 'remove' in request.POST:
    process.samples.remove(sample)
  
  return HttpResponse(status=200)


@login_required(login_url='login')
def review_process(request, username, pk):
  pass


@login_required(login_url='login')
def tcprotocols(request):
  protocols = ThermalCyclerProtocol.objects.filter(user=request.user)
  context = {'protocols': protocols}
  return render(request, 'pcr/tcprotocols.html', context)


@login_required(login_url='login')
def create_tcprotocol(request):
  form = ThermalCyclerProtocolForm()
  
  if request.method == "POST":
    form = ThermalCyclerProtocolForm(request.POST)
    if form.is_valid():
      protocol = form.save(commit=False)
      protocol.user = request.user
      protocol.save()
      return redirect('tcprotocols')
    else:
      print(form.errors)
  
  context = {'form': form}
  return render(request, 'pcr/create_tcprotocol.html', context)


@login_required(login_url='login')
def edit_tcprotocol(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no thermal cycler protocol to edit.")
    return redirect('tcprotocols')
  
  try:
    protocol = ThermalCyclerProtocol.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no thermal cycler protocol to edit.")
    return redirect('tcprotocols')
  
  form = ThermalCyclerProtocolForm(instance=protocol)
  del_form = DeletionForm(value=protocol.name)
 
  if 'update' in request.POST:
    form = ThermalCyclerProtocolForm(request.POST, instance=protocol)
    if form.is_valid():
      form.save()
      return redirect('tcprotocols')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=protocol.name)
    if del_form.is_valid():
      protocol.delete()
      return redirect('tcprotocols')
    else:
      print(del_form.errors)

  context = {'form': form, 'del_form': del_form, 'protocol': protocol}
  return render(request, 'pcr/edit_tcprotocol.html', context)