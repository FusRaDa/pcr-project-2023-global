from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.models import User

from ..models.assay import Assay, Fluorescence, Control
from ..forms.assay import AssayForm, ReagentAssay, ReagentAssayForm, FluorescenceForm, ControlForm
from ..forms.general import DeletionForm

@login_required(login_url='login')
def assays(request):
  pcr_dna = Assay.objects.filter(user=request.user, method=Assay.Methods.PCR, type=Assay.Types.DNA).order_by('name')
  pcr_rna = Assay.objects.filter(user=request.user, method=Assay.Methods.PCR, type=Assay.Types.RNA).order_by('name')
  qpcr_dna = Assay.objects.filter(user=request.user, method=Assay.Methods.qPCR, type=Assay.Types.DNA).order_by('name')
  qpcr_rna = Assay.objects.filter(user=request.user, method=Assay.Methods.qPCR, type=Assay.Types.RNA).order_by('name')

  context = {'pcr_dna': pcr_dna, 'pcr_rna': pcr_rna, 'qpcr_dna': qpcr_dna, 'qpcr_rna': qpcr_rna}
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
  del_form = DeletionForm(value=assay.name)

  if 'update' in request.POST:
    form = AssayForm(request.POST, user=request.user, instance=assay)
    if form.is_valid():
      form.save()
      return redirect('assay_through', request.user.username, pk)
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=assay.name)
    if del_form.is_valid():
      assay.delete()
      return redirect('assays')
    else:
      print(del_form.errors)
  
  context = {'assay': assay, 'form': form, 'del_form': del_form}
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
      return redirect('assays')
    else:
      print(reagentformset.errors)
      print(reagentformset.non_form_errors())
        
  context = {'reagentformset': reagentformset, 'reagents_data': reagents_data, 'assay': assay}
  return render(request, 'assay/assay_through.html', context)


@login_required(login_url='login')
def fluorescence(request):
  fluorescence = Fluorescence.objects.filter(user=request.user).order_by('name')

  context = {'fluorescence': fluorescence}
  return render(request, 'assay/fluorescence.html', context)


@login_required(login_url='login')
def create_fluorescence(request):
  context = {}
  form = FluorescenceForm()

  if request.method == "POST":
    form = FluorescenceForm(request.POST)
    if form.is_valid():
      flourescence = form.save(commit=False)
      flourescence.user = request.user
      flourescence = form.save()
      return redirect('fluorescence')
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'assay/create_fluorescence.html', context)


@login_required(login_url='login')
def edit_fluorescence(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no flourescence to edit.")
    return redirect('flourescence')
  
  try:
    fluorescence = Fluorescence.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no flourescence to edit.")
    return redirect('fluorescence')
  
  form = FluorescenceForm(instance=fluorescence)
  del_form = DeletionForm(value=fluorescence.name)

  if 'update' in request.POST:
    form = FluorescenceForm(request.POST, instance=fluorescence)
    if form.is_valid():
      form.save()
      return redirect('fluorescence')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=fluorescence.name)
    if del_form.is_valid():
      fluorescence.delete()
      return redirect('fluorescence')
    else:
      print(del_form.errors)

  context = {'form': form, 'fluorescence': fluorescence, 'del_form': del_form}
  return render(request, 'assay/edit_fluorescence.html', context)


@login_required(login_url='login')
def controls(request):
  controls = Control.objects.filter(user=request.user).order_by(F('exp_date').asc(nulls_last=True))

  context = {'controls': controls}
  return render(request, 'assay/controls.html', context)


@login_required(login_url='login')
def create_control(request):
  context = {}
  form = ControlForm(user=request.user)

  if request.method == "POST":
    form = ControlForm(request.POST, user=request.user)
    if form.is_valid():
      control = form.save(commit=False)
      control.user = request.user
      control = form.save()
      return redirect('controls')
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'assay/create_control.html', context)


@login_required(login_url='login')
def edit_control(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no control to edit.")
    return redirect('controls')
  
  try:
    control = Control.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no control to edit.")
    return redirect('controls')
  
  form = ControlForm(instance=control, user=request.user)
  del_form = DeletionForm(value=control.name)

  if 'update' in request.POST:
    form = ControlForm(request.POST, user=request.user, instance=control)
    if form.is_valid():
      form.save()
      return redirect('controls')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=control.name)
    if del_form.is_valid():
      control.delete()
      return redirect('controls')
    else:
      print(del_form.errors)

  context = {'form': form, 'control': control, 'del_form': del_form}
  return render(request, 'assay/edit_control.html', context)