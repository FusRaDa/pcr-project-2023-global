from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from ..models.inventory import Reagent
from ..models.batch import Batch, Sample
from ..forms.batch import BatchForm, SampleForm, SampleAssayForm, NumberSamplesForm
from ..forms.general import DeletionForm
from ..custom.functions import create_samples, send_theshold_alert_email_ext


@login_required(login_url='login')
def batches(request):
  batches = Batch.objects.filter(user=request.user, is_extracted=False).order_by('-date_created')
  context = {'batches': batches}
  return render(request, 'batch/batches.html', context)


@login_required(login_url='login')
def create_batch(request):
  form = BatchForm(user=request.user)

  batches = Batch.objects.filter(user=request.user).order_by('-lab_id')[:10]

  if request.method == "POST":
    form = BatchForm(request.POST, user=request.user)

    if form.is_valid():
      extraction_protocol_dna = form.cleaned_data['extraction_protocol_dna']
      extraction_protocol_rna = form.cleaned_data['extraction_protocol_rna']
      extraction_protocol_tn = form.cleaned_data['extraction_protocol_tn']
      lab_id = form.cleaned_data['lab_id']
      negative_control = form.cleaned_data['negative_control']

      batch = form.save(commit=False)
      batch.user = request.user

      if extraction_protocol_dna:
        batch.extraction_protocol = extraction_protocol_dna

      if extraction_protocol_rna:
        batch.extraction_protocol = extraction_protocol_rna

      if extraction_protocol_tn:
        batch.extraction_protocol = extraction_protocol_tn

      batch = form.save()

      number_of_samples = form.cleaned_data['number_of_samples']
      lab_id = form.cleaned_data['lab_id']

      create_samples(
        number_of_samples=number_of_samples, 
        lab_id=lab_id, 
        user=request.user,
        negative_control=negative_control,
      )

      return redirect('batch_samples', pk=batch.pk)
    else:
      print(form.errors)
  
  context = {'form': form, 'batches': batches}
  return render(request, 'batch/create_batch.html', context)


@login_required(login_url='login')
def batch_samples(request, pk):
  SampleFormSet = inlineformset_factory(
    Batch, 
    Sample, 
    form=SampleForm,
    extra=0, 
    can_delete=False,
    )
  formset = None

  try:
    batch = Batch.objects.get(user=request.user, pk=pk)
    if batch.is_extracted:
      messages.error(request, "This batch has already been processed for extraction and can no longer be updated or deleted.")
      return redirect('batches')
  except ObjectDoesNotExist:
    messages.error(request, "There is no batch to view.")
    return redirect('batches')

  samples = batch.sample_set.all()

  extractable = False
  for sample in samples:
    if sample.sample_id == "" or sample.sample_id == None:
      extractable = True
      break

  formset = SampleFormSet(instance=batch)
  del_form = DeletionForm(value=batch.name)
  samplesform = NumberSamplesForm()

  data = zip(samples, formset)

  if 'update' in request.POST:
    formset = SampleFormSet(request.POST, instance=batch)
    if formset.is_valid():
      formset.save()
      return redirect(request.path_info)
    else:
      print(formset.errors)
      print(formset.non_form_errors())

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=batch.name)
    if del_form.is_valid():
      batch.delete()
      return redirect('batches')
    else:
      print(del_form.errors)

  if 'number-of-samples' in request.POST:
    samplesform = NumberSamplesForm(request.POST)
    if samplesform.is_valid():
      number_of_samples = samplesform.cleaned_data['number_of_samples']
      lab_id = batch.lab_id

      for sample in samples:
        sample.delete()

      create_samples(
        number_of_samples=number_of_samples, 
        lab_id=lab_id, 
        user=request.user,
        negative_control=batch.negative_control
      )

    return redirect(request.path_info)
  
  if 'extracted' in request.POST:
    # **VALIDATE** #
    invalid_samples = False
    for sample in samples:
      if not sample.sample_id:
        invalid_samples = True

    if invalid_samples:
      messages.error(request, "All samples must have an ID.")
    
    invalid_items = False
    for reagent in batch.extraction_protocol.reagentextraction_set.all():
      if reagent.reagent.is_expired:
        invalid_items = True
        messages.error(request, f'Reagent: {reagent.reagent.name} is expired. Either update the <a href="/edit-extraction-protocol/{batch.extraction_protocol.pk}" target="_blank"> protocol </a> or <a href="/edit-reagent/{reagent.reagent.pk}" target="_blank">reagent.</a>')
      
      total_used_reagents = reagent.amount_per_sample * batch.sample_set.count()
      rem_reagents = reagent.reagent.volume_in_microliters - total_used_reagents
      if rem_reagents < 0:
        invalid_items = True
        messages.error(request, f'The amount of {reagent.reagent.name} lot#{reagent.reagent.lot_number} is insufficent. At least {total_used_reagents}µl is required. Either update the <a href="/edit-extraction-protocol/{batch.extraction_protocol.pk}" target="_blank"> protocol </a> or <a href="/edit-reagent/{reagent.reagent.pk}" target="_blank">reagent.</a>')
      
    for tube in batch.extraction_protocol.tubeextraction_set.all():
      if tube.tube.is_expired:
        invalid_items = True
        messages.error(request, f'Tube: {tube.tube.name} is expired. Either update the <a href="/edit-extraction-protocol/{batch.extraction_protocol.pk}" target="_blank"> protocol </a> or <a href="/edit-tube/{tube.tube.pk}" target="_blank"> tube.</a>')
      
      total_used_tubes = tube.amount_per_sample * batch.sample_set.count()
      rem_tubes = tube.tube.amount - total_used_tubes
      if rem_tubes < 0:
        invalid_items = True
        messages.error(request, f'The amount of {tube.tube.name} lot#{tube.tube.lot_number} is insufficent. At least {total_used_tubes} is required. Either update the <a href="/edit-extraction-protocol/{batch.extraction_protocol.pk}" target="_blank"> protocol </a> or <a href="/edit-tube/{tube.tube.pk}" target="_blank"> tube.</a>')
    
    if invalid_samples or invalid_items:
      return redirect(request.path_info)
    # **VALIDATE** #
      
    batch.is_extracted = True

    # **ALERT DATA** #
    inventory_alerts = {
      'date': batch.date_created,
      'reagents': [],
      'tubes': [],
    }

    # **FINAL UPDATE OF DB** #
    for reagent in batch.extraction_protocol.reagentextraction_set.all():
      total_used_reagents = reagent.amount_per_sample * batch.sample_set.count()

      if reagent.reagent.threshold > 0:
        diff = reagent.reagent.volume_in_microliters - total_used_reagents - reagent.reagent.threshold_in_microliters
        reagent.reagent.threshold_diff = diff

        if diff <= 0 or reagent.reagent.month_exp:
          inventory_alerts['reagents'].append({
            'exp': reagent.reagent.month_exp,
            'pk': reagent.reagent.pk,
            'name': reagent.reagent.name, 
            'lot': reagent.reagent.lot_number,
            'cat': reagent.reagent.catalog_number,
            'amount': reagent.reagent.volume,
          })

      reagent.reagent.volume = reagent.reagent.volume_in_microliters - total_used_reagents

      reagent.reagent.unit_volume = Reagent.VolumeUnits.MICROLITER
      reagent.reagent.save()
    
    for tube in batch.extraction_protocol.tubeextraction_set.all():
      total_used_tubes = tube.amount_per_sample * batch.sample_set.count()

      if tube.tube.threshold > 0:
        diff = tube.tube.amount - total_used_tubes - tube.tube.threshold
        tube.tube.threshold_diff = diff

        if diff <= 0 or tube.tube.month_exp:
          inventory_alerts['tubes'].append({
            'exp': tube.tube.month_exp,
            'pk': tube.tube.pk,
            'name': tube.tube.name, 
            'lot': tube.tube.lot_number,
            'cat': tube.tube.catalog_number,
            'amount': tube.tube.amount,
          })

      tube.tube.amount -= total_used_tubes
      tube.tube.save()
    # **FINAL UPDATE OF DB** #

    if inventory_alerts['reagents'] or inventory_alerts['tubes']:
      send_theshold_alert_email_ext(request, inventory_alerts)
    # **ALERT DATA** #
      
    batch.save()
    return redirect('extracted_batches')

  context = {'batch': batch, 'data': data, 'formset': formset, 'del_form': del_form, 'samplesform': samplesform, 'extractable': extractable}
  return render(request, 'batch/batch_samples.html', context)


@login_required(login_url='login')
def batch_paperwork(request, pk):
  try:
    batch = Batch.objects.get(user=request.user, pk=pk)
    protocol = batch.extraction_protocol

    panel = batch.code.assays.all()
    samples_num = []
    controls_num = []
    samples_per_assay = []
    for assay in panel:
      samples = assay.sample_set.filter(batch=batch).count()
      controls = assay.controls.count()

      samples_num.append(samples)
      controls_num.append(controls)

      sum = controls + samples
      samples_per_assay.append(sum)

    assays = zip(panel, samples_per_assay, samples_num, controls_num)

  except ObjectDoesNotExist:
    messages.error(request, "There is no batch to view.")
    return redirect('batches')
  
  context = {'batch': batch, 'protocol': protocol, 'assays': assays}
  return render(request, 'batch/batch_paperwork.html', context)


@login_required(login_url='login')
def sample_assay(request, pk):
  try:
    sample = Sample.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no sample to edit.")
    return redirect('batches')
  
  form = SampleAssayForm(user=request.user, instance=sample)
  
  if request.method == 'POST':
    form = SampleAssayForm(request.POST, user=request.user, instance=sample)
    if form.is_valid():
      form.save()

      pcr_dna = form.cleaned_data['pcr_dna']
      pcr_rna = form.cleaned_data['pcr_rna']
      qpcr_dna = form.cleaned_data['qpcr_dna']
      qpcr_rna = form.cleaned_data['qpcr_rna']

      assays = pcr_dna | pcr_rna | qpcr_dna | qpcr_rna

      sample.assays.clear()
      for assay in assays:
        sample.assays.add(assay)

      if sample.batch.negative_control == True:
      # Ensure neg ctrl sample has all assays #
        sample_assays = []  
        for sample in sample.batch.sample_set.all()[:sample.batch.sample_set.count()-1]:
          for assay in sample.assays.all():
            sample_assays.append(assay)
        set_sample_assays = set(sample_assays)

        neg_sample = sample.batch.sample_set.all().last()

        neg_sample.assays.clear()
        for assay in set_sample_assays:
          neg_sample.assays.add(assay)
        neg_sample.save()
        # Ensure neg ctrl sample has all assays #

      return redirect('batch_samples', sample.batch.pk)
    else:
      print(form.errors)

  context = {'form': form, 'sample': sample}
  return render(request, 'batch/sample_assay.html', context)