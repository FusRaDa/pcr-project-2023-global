from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib import messages

from .models import *
from .forms import *
from .functions import create_samples


# Create your views here.

# **START OF SAMPLE FUNCTIONALITY** #
@login_required(login_url='login')
def viewBatches(request):

  batches = Batch.objects.filter(user=request.user).order_by('-date_created')

  context = {'batches': batches}
  return render(request, 'batches.html', context)


@login_required(login_url='login')
def createBatches(request):

  form = BatchForm(user=request.user)

  if request.method == "POST":
    form = BatchForm(request.POST, user=request.user)

    if form.is_valid():

      batch = form.save(commit=False)
      batch.user = request.user
      batch = form.save()

      number_of_samples = form.cleaned_data['number_of_samples']
      lab_id = form.cleaned_data['lab_id']

      create_samples(
        number_of_samples=number_of_samples, 
        lab_id=lab_id, 
        user=request.user,
      )

      return redirect('batch_samples', username=request.user.username, pk=batch.id)
    
  else:
    for error in list(form.errors.values()):
      messages.error(request, error)
  
  context = {'form': form}
  return render(request, 'create_batch.html', context)


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

  if request.method == 'POST':
    formset = SampleFormSet(request.POST, instance=batch)
    if formset.is_valid():
      formset.save()
      return redirect('batches')
    else:
      print(formset.errors)
      print(formset.non_form_errors())
   
  context = {'batch': batch, 'data': data, 'formset': formset}

  return render(request, 'batch_samples.html', context)


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
  pk = sample.batch.pk

  if request.method == 'POST':
    form = SampleAssayForm(request.POST, user=request.user, instance=sample)
    if form.is_valid():
      form.save()
      return redirect('batch_samples', request.user.username, pk)
    else:
      print(form.errors)

  context = {'form': form, 'sample': sample}

  return render(request, 'sample_assay.html', context)
# **END OF SAMPLE FUNCTIONALITY** #


# **START OF ASSAY FUNCTIONALITY** #
def protocols(request):
  
  context = {}
  return render(request, 'protocols.html', context)


# **END OF ASSAY FUNCTIONALITY** #



