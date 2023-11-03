from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .forms import *
from .functions import create_samples


# Create your views here.
@login_required(login_url='login')
def viewBatches(request):

  batches = Batch.objects.filter(username=request.user.username)

  context = {'batches': batches}
  return render(request, 'batches.html', context)


@login_required(login_url='login')
def createBatches(request):

  user = request.user
  form = CreateBatchForm()

  if request.method == "POST":
    form = CreateBatchForm(request.POST)

    if form.is_valid():
      batch = form.save(commit=False)
      batch.user = user
      batch.save()

      number_of_samples = form.cleaned_data['number_of_samples']
      lab_id = form.cleaned_data['lab_id']

      create_samples(
        number_of_samples=number_of_samples, 
        lab_id=lab_id, 
        user=user,
      )
      
      return redirect('batch_samples')
    
  else:
    for error in list(form.errors.values()):
      messages.error(request, error)
  
  context = {'form': form}
  return render(request, 'batches.html', context)


@login_required(login_url='login')
def batchSamples(request, pk):

  batch = Batch.objects.get(pk=pk)
  samples = batch.sample_set.all()

  context = {'samples': samples}
  return render(request, 'batch_samples.html', context)

 




