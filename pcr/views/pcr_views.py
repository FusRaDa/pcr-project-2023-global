from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.http import HttpResponse
from django.contrib import messages
from users.models import User

from ..forms.general import DeletionForm
from ..forms.pcr import ThermalCyclerProtocolForm, ProcessForm
from ..models.pcr import ThermalCyclerProtocol, Process
from ..models.batch import Batch, Sample
from ..models.assay import Assay
from ..custom.functions import samples_by_assay, dna_pcr_samples, json_organized_horizontal_plate


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
def edit_tcprotocol(request, pk):
  try:
    protocol = ThermalCyclerProtocol.objects.get(user=request.user, pk=pk)
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
def add_batch_samples(request, process_pk, batch_pk):
  try:
    batch = Batch.objects.get(user=request.user, pk=batch_pk)
    process = Process.objects.get(user=request.user, pk=process_pk, is_processed=False)
  except ObjectDoesNotExist:
    messages.error(request, "There is no sample or process found.")
    return redirect('extracted_batches')
  
  if 'all' in request.POST:
    added_samples = []
    samples = batch.sample_set.all()
    for sample in samples:
      if not process.samples.contains(sample):
        process.samples.add(sample)
        added_samples.append(sample)

    context = {'added_samples': added_samples, 'process': process}
    return render(request, 'pcr/batch_in_process.html', context)
      
  return HttpResponse(status=200)


@login_required(login_url='login')
def add_sample_to_process(request, process_pk, sample_pk):
  try:
    sample = Sample.objects.get(user=request.user, pk=sample_pk)
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
def remove_sample_from_process(request, process_pk, sample_pk):
  try:
    sample = Sample.objects.get(user=request.user, pk=sample_pk)
    process = Process.objects.get(user=request.user, is_processed=False, pk=process_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no sample or process found.")
    return redirect('extracted_batches')
  
  if 'remove' in request.POST:
    process.samples.remove(sample)
  
  return HttpResponse(status=200)


@login_required(login_url='login')
def review_process(request, pk):
  try:
    process = Process.objects.get(user=request.user, is_processed=False, pk=pk)
    samples = process.samples.all().order_by('lab_id_num')

    if samples.count() < 1:
      messages.error(request, "Process must have at least one sample.")
      return redirect('extracted_batches')
  
    assay_samples = samples_by_assay(samples)
  except ObjectDoesNotExist:
    messages.error(request, "There is no process to review.")
    return redirect('extracted_batches')
  
  form = ProcessForm(instance=process, user=request.user)

  if request.method == 'POST':
    form = ProcessForm(request.POST, instance=process, user=request.user)
    if form.is_valid():
      form.save()
      return redirect('process_paperwork', process.pk)
    else:
      print(form.errors)
  
  context = {'form': form, 'assay_samples': assay_samples, 'process':  process}
  return render(request, 'pcr/review_process.html', context)


@login_required(login_url='login')
def process_paperwork(request, pk):
  try:
    process = Process.objects.get(user=request.user, pk=pk)
    samples = process.samples.all().order_by('lab_id_num')
    assay_samples = samples_by_assay(samples)

    requires_dna_pcr = False
    requires_rna_pcr = False
    requires_dna_qpcr = False
    requires_rna_qpcr = False

    for assay in assay_samples:
      for a in assay.keys():
        if a.type == Assay.Types.DNA and a.method == Assay.Methods.PCR:
          requires_dna_pcr = True
        if a.type == Assay.Types.RNA and a.method == Assay.Methods.PCR: 
          requires_rna_pcr = True
        if a.type == Assay.Types.DNA and a.method == Assay.Methods.qPCR:
          requires_dna_qpcr = True
        if a.type == Assay.Types.RNA and a.method == Assay.Methods.qPCR:
          requires_rna_qpcr = True
    
    if requires_dna_pcr:
      all_samples = dna_pcr_samples(assay_samples)
      dna_pcr_json = json_organized_horizontal_plate(all_samples, process)


    # if requires_rna_pcr:
    #   print("RNA PCR")

    # if requires_dna_qpcr:
    #   print("DNA qPCR")
    
    # if requires_rna_qpcr:
    #   print("RNA qPCR")

  except ObjectDoesNotExist:
    messages.error(request, "There is no process to review.")
    return redirect('extracted_batches')
  
  context = {'dna_pcr_json': dna_pcr_json}
  return render(request, 'pcr/process_paperwork.html', context)