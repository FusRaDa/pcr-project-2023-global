from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User

from ..models.batch import Batch, Sample
from ..forms.batch import BatchForm, SampleForm, SampleAssayForm
from ..forms.general import DeletionForm
from ..custom.functions import create_samples


@login_required(login_url='login')
def viewBatches(request):
  batches = Batch.objects.filter(user=request.user).order_by('-date_created')

  context = {'batches': batches}
  return render(request, 'batch/batches.html', context)


@login_required(login_url='login')
def createBatches(request):
  form = BatchForm(user=request.user)

  if request.method == "POST":
    form = BatchForm(request.POST, user=request.user)

    if form.is_valid():
      extraction_protocol_dna = form.cleaned_data['extraction_protocol_dna']
      extraction_protocol_rna = form.cleaned_data['extraction_protocol_rna']
      extraction_protocol_tn = form.cleaned_data['extraction_protocol_tn']

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
      )

      return redirect('batch_samples', username=request.user.username, pk=batch.pk)
    else:
      print(form.errors)
  
  context = {'form': form}
  return render(request, 'batch/create_batch.html', context)


@login_required(login_url='login')
def deleteBatch(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no batch to delete.")
    return redirect('batches')
  
  try:
    batch = Batch.objects.get(user=user, pk=pk)
    batch.delete()
  except ObjectDoesNotExist:
    messages.error(request, "There is no batch to delete.")
    return redirect('batches')

  return redirect('batches')


@login_required(login_url='login')
def batchSamples(request, username, pk):
  context = {}
  SampleFormSet = inlineformset_factory(
    Batch, 
    Sample, 
    form=SampleForm,
    extra=0, 
    can_delete=False,
    )
  formset = None

  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no batch to view.")
    return redirect('batches')
  
  try:
    batch = Batch.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no batch to view.")
    return redirect('batches')

  samples = batch.sample_set.all()
  formset = SampleFormSet(instance=batch)

  data = zip(samples, formset)

  if 'update' in request.POST:
    formset = SampleFormSet(request.POST, instance=batch)
    if formset.is_valid():
      formset.save()
      return redirect('batches')
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
   
  context = {'batch': batch, 'data': data, 'formset': formset}
  return render(request, 'batch/batch_samples.html', context)


@login_required(login_url='login')
def editSampleAssay(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no sample to edit.")
    return redirect('batches')
  
  try:
    sample = Sample.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no sample to edit.")
    return redirect('batches')
  
  form = SampleAssayForm(user=request.user, instance=sample)
  
  if request.method == 'POST':
    form = SampleAssayForm(request.POST, user=request.user, instance=sample)
    if form.is_valid():
      form.save()
      return redirect('batch_samples', request.user.username, sample.batch.pk)
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'batch/sample_assay.html', context)