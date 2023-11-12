from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .models import *
from .forms import *
from .functions import create_samples


# Create your views here.
@login_required(login_url='login')
def viewBatches(request):

  batches = Batch.objects.filter(user=request.user).order_by('date_created')

  context = {'batches': batches}
  return render(request, 'batches.html', context)


@login_required(login_url='login')
def createBatches(request):

  user = request.user
  form = BatchForm()

  if request.method == "POST":
    form = BatchForm(request.POST)

    if form.is_valid():
      batch = form.save(commit=False)
      batch.user = user
      batch = form.save()

      number_of_samples = form.cleaned_data['number_of_samples']
      lab_id = form.cleaned_data['lab_id']

      create_samples(
        number_of_samples=number_of_samples, 
        lab_id=lab_id, 
        user=user,
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
      print(formset.data)
      formset.save()
      return redirect('batches')
    else:
      print(formset.errors)
      print(formset.non_form_errors())
   
  context = {'batch': batch, 'data': data, 'formset': formset}

  return render(request, 'batch_samples.html', context)

 




