from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from users.models import User

from ..forms.general import DeletionForm, SearchProcessForm, SearchBatchForm
from ..forms.pcr import ThermalCyclerProtocolForm, ProcessForm
from ..models.pcr import ThermalCyclerProtocol, Process
from ..models.batch import Batch, Sample
from ..models.assay import Assay
from ..models.inventory import Gel, Plate
from ..custom.functions import samples_by_assay, dna_pcr_samples, rna_pcr_samples, dna_qpcr_samples, rna_qpcr_samples, process_qpcr_samples, process_pcr_samples


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
  process = Process.objects.filter(user=request.user, is_processed=False)
  if not process.exists():
    process = Process.objects.create(user=request.user)
  else:
    process = Process.objects.get(user=request.user, is_processed=False)

  batches = Batch.objects.filter(user=request.user, is_extracted=True).order_by('-date_created')

  if 'clear' in request.POST:
    process.samples.clear()
    return redirect(request.path_info)
  
  form = SearchBatchForm(user=request.user)
  if 'search' in request.POST:
    form = SearchBatchForm(request.POST, user=request.user)
    if form.is_valid():
      name = form.cleaned_data['name']
      lab_id = form.cleaned_data['lab_id']
      panel = form.cleaned_data['panel']
      protocol = form.cleaned_data['extraction_protocol']
      start_date = form.cleaned_data['start_date']
      end_date = form.cleaned_data['end_date']

      filters = {}
      if name:
        filters['name__icontains'] = name
      if panel:
        filters['code'] = panel
      if lab_id:
        filters['lab_id'] = lab_id
      if protocol:
        filters['extraction_protocol'] = protocol
      
      if start_date and not end_date:
        day = start_date + datetime.timedelta(days=1)
        filters['date_created__range'] = [start_date, day]

      if end_date and not start_date:
        day = end_date + datetime.timedelta(days=1)
        filters['date_created__range'] = [end_date, day]
      
      if start_date and end_date:
        end_date += datetime.timedelta(days=1)
        filters['date_created__range'] = [start_date, end_date]

      batches = Batch.objects.filter(**filters, is_extracted=True).order_by('-date_created')
    else:
      print(form.errors)

  paginator = Paginator(batches, 10)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'process': process, 'form': form}
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
  except ObjectDoesNotExist:
    messages.error(request, "There is no process to review.")
    return redirect('extracted_batches')
  
  samples = process.samples.all()
  if samples.count() < 1:
    messages.error(request, "Process must have at least one sample.")
    return redirect('extracted_batches')

  assay_samples = samples_by_assay(samples)
  
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
  except ObjectDoesNotExist:
    messages.error(request, "There is no process to review.")
    return redirect('extracted_batches')
  
  samples = process.samples.all()
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

  plates = []
  for plate in process.plate.all().order_by('size'):
    plates.append({'plate': plate, 'name': plate.name, 'catalog_number': plate.catalog_number, 'lot_number': plate.lot_number, 'size': plate.size, 'amount': plate.amount, 'used': 0})

  dna_pcr_json = None
  if requires_dna_pcr:
    samples_dna_pcr = dna_pcr_samples(assay_samples)
    dna_pcr_json = process_pcr_samples(samples_dna_pcr, process, process.pcr_dna_protocol, process.min_samples_per_gel_dna)

  rna_pcr_json = None
  if requires_rna_pcr:
    samples_rna_pcr = rna_pcr_samples(assay_samples)
    rna_pcr_json = process_pcr_samples(samples_rna_pcr, process, process.pcr_rna_protocol, process.min_samples_per_gel_rna)
  
  dna_qpcr_json = None
  if requires_dna_qpcr:
    samples_dna_qpcr = dna_qpcr_samples(assay_samples)
    dna_qpcr_json = process_qpcr_samples(samples_dna_qpcr, plates, process.qpcr_dna_protocol, process.min_samples_per_plate_dna)

  rna_qpcr_json = None
  if requires_rna_qpcr:
    samples_rna_qpcr = rna_qpcr_samples(assay_samples)
    rna_qpcr_json = process_qpcr_samples(samples_rna_qpcr, plates, process.qpcr_rna_protocol, process.min_samples_per_plate_rna)

  is_insufficient = False
  for plate in plates:
    if plate['amount'] < 0:
      is_insufficient = True

  if 'process' in request.POST:

    if is_insufficient:
      messages.error(request, "Your plate inventory is insufficent for this process. Please update and try again.")
      return redirect(request.path_info)

    # process.is_processed = True
    process.date_processed = timezone.now()

    process.pcr_dna_json = dna_pcr_json
    process.pcr_rna_json = rna_pcr_json
    process.qpcr_dna_json = dna_qpcr_json
    process.qpcr_rna_json = rna_qpcr_json

    array = []
    for sample in process.samples.all():
      array.append(sample.batch)
    batches = list(set(array))

    process.batches.clear()
    for batch in batches:
      process.batches.add(batch)
    
    process.save()
    return redirect('processes')

  context = {'dna_qpcr_json': dna_qpcr_json, 'rna_qpcr_json': rna_qpcr_json, 'dna_pcr_json': dna_pcr_json, 'rna_pcr_json': rna_pcr_json, 'plates': plates}
  return render(request, 'pcr/process_paperwork.html', context)


@login_required(login_url='login')
def processes(request):
  processes = Process.objects.filter(user=request.user, is_processed=True).order_by('-date_processed')

  form = SearchProcessForm(user=request.user)
  if request.method == "POST":
    form = SearchProcessForm(request.POST, user=request.user)
    if form.is_valid():
      name = form.cleaned_data['name']
      panel = form.cleaned_data['panel']
      lab_id = form.cleaned_data['lab_id']
      start_date = form.cleaned_data['start_date']
      end_date = form.cleaned_data['end_date']

      filters = {}
      if name:
        filters['name__icontains'] = name
      if panel:
        filters['batches__code'] = panel
      if lab_id:
        filters['batches__lab_id'] = lab_id

      if start_date and not end_date:
        day = start_date + datetime.timedelta(days=1)
        filters['date_processed__range'] = [start_date, day]

      if end_date and not start_date:
        day = end_date + datetime.timedelta(days=1)
        filters['date_processed__range'] = [end_date, day]
      
      if start_date and end_date:
        end_date += datetime.timedelta(days=1)
        filters['date_processed__range'] = [start_date, end_date]

      processes = Process.objects.filter(**filters, is_processed=True).order_by('-date_processed')
    else:
      print(form.errors)

  paginator = Paginator(processes, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  
  context = {'page_obj': page_obj, 'form': form}
  return render(request, 'pcr/processes.html', context)


@login_required(login_url='login')
def pcr_paperwork(request, pk):
  try:
    process = Process.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no process to review.")
    return redirect('processes')
  
  context = {'dna_qpcr_json': process.qpcr_dna_json, 'rna_qpcr_json': process.qpcr_rna_json, 'dna_pcr_json': process.pcr_dna_json, 'rna_pcr_json': process.pcr_rna_json, 'process': process}
  return render(request, 'pcr/pcr_paperwork.html', context)