from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User

from ..models.assay import Assay
from ..forms.assay import AssayForm, ReagentAssay, ReagentAssayForm


@login_required(login_url='login')
def assays(request):
  assays = Assay.objects.filter(user=request.user).order_by('name')

  context = {'assays': assays}
  return render(request, 'assay/assays.html', context)


@login_required(login_url='login')
def create_assay(request):
  context = {}
  form = AssayForm(user=request.user)

  if request.method == "POST":
    form = AssayForm(request.POST, user=request.user)
    if form.is_valid():
      assay = form.save(commit=False)
      assay.user = request.user
      assay = form.save()
      return redirect('assay_through', request.user, assay.pk)
  else:
    print(form.errors)

  context = {'form': form}
  return render(request, 'assay/create_assay.html', context)


@login_required(login_url='login')
def edit_assay(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no assay to edit.")
    return redirect('assays')
  
  try:
    assay = Assay.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no assay to edit.")
    return redirect('assays')
  
  form = AssayForm(user=request.user, instance=assay)

  if request.method == 'POST':
    form = AssayForm(request.POST, user=request.user, instance=assay)
    if form.is_valid():
      form.save()
      return redirect('assay_through', request.user.username, pk)
    else:
      print(form.errors)
  
  context = {'assay': assay, 'form': form}
  return render(request, 'assay/edit_assay.html', context)


@login_required(login_url='login')
def assay_through(request, username, pk):
  context = {}

  ReagentAssayFormSet = modelformset_factory(
    ReagentAssay,
    form=ReagentAssayForm,
    extra=0,
    )
  
  reagentformset = None

  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no assay to edit.")
    return redirect('extraction_protocols')
  
  try:
    assay = Assay.objects.get(user=user, pk=pk)
    reagents = ReagentAssay.objects.prefetch_related('reagent', 'assay').filter(assay=assay).order_by('-order')
  except ObjectDoesNotExist:
    messages.error(request, "There is no assay to edit.")
    return redirect('extraction_protocols')
  
  reagentformset = ReagentAssayFormSet(queryset=reagents)

  reagents_data = zip(reagents, reagentformset)

  if request.method == "POST":
    reagentformset = ReagentAssayFormSet(request.POST)
    if reagentformset.is_valid():
      reagentformset.save()
      messages.success(request, "Reagent quantity and order have been modified/saved!")
      return redirect(request.path_info)
    else:
      print(reagentformset.errors)
      print(reagentformset.non_form_errors())

  context = {'reagentformset': reagentformset, 'reagents_data': reagents_data, 'assay': assay}
  return render(request, 'assay/assay_through.html', context)


@login_required(login_url='login')
def delete_assay(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no assay to delete.")
    return redirect('assays')
  
  try:
    assay = Assay.objects.get(user=user, pk=pk)
    assay.delete()
  except ObjectDoesNotExist:
    messages.error(request, "There is no assay to delete.")
    return redirect('assays')

  return redirect('assays')