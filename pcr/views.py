from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
def deleteBatch(username, pk):

  try:
    user = User.objects.get(username=username)
    batch = Batch.objects.get(user=user, pk=pk)
    batch.delete()
    return redirect('batches')
  except ObjectDoesNotExist:
    return redirect('batches')
  

@login_required(login_url='login')
def batchSamples(request, username, pk):

  context = {}

  try:
    user = User.objects.get(username=username)
    batch = Batch.objects.get(user=user, pk=pk)
    samples = batch.sample_set.all()
    context = {'samples': samples, "batch": batch}
  except ObjectDoesNotExist:
    return redirect('batches')

  return render(request, 'batch_samples.html', context)

 




