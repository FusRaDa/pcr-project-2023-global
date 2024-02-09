from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

from ..models.inventory import Reagent
from ..models.assay import Assay, Fluorescence, Control, ControlAssay, ReagentAssay
from ..forms.assay import AssayForm, ReagentAssayForm, FluorescenceForm, ControlForm, ControlAssayForm
from ..forms.general import DeletionForm, SearchAssayForm, SearchControlForm, SearchFluorescenseForm, TextSearchForm


@login_required(login_url='login')
def assays(request):
  assays = Assay.objects.filter(user=request.user).order_by('name')

  form = SearchAssayForm()
  if request.method == "GET":
    form = SearchAssayForm(request.GET)
    if form.is_valid():
      name = form.cleaned_data['name']
      method = form.cleaned_data['method']
      type = form.cleaned_data['type']

      filters = {}
      if name:
        filters['name__icontains'] = name
      if method:
        filters['method'] = method
      if type:
        filters['type'] = type
      assays = Assay.objects.filter(**filters, user=request.user).order_by('name')

  paginator = Paginator(assays, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'form': form}
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

      # reagents = assay.reagentassay_set.all()
      # for reagent in reagents:
      #   reagent.final_concentration_unit = reagent.reagent.unit_concentration
      #   reagent.save()

      return redirect('edit_assay', assay.pk)
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'assay/create_assay.html', context)


@login_required(login_url='login')
def edit_assay(request, pk):
  try:
    assay = Assay.objects.get(user=request.user, pk=pk)
    assay_reagents = assay.reagentassay_set.all()
    assay_controls = assay.controlassay_set.all()
  except ObjectDoesNotExist:
    messages.error(request, "There is no assay to edit.")
    return redirect('assays')
  
  reagents = Reagent.objects.filter(user=request.user, usage=Reagent.Usages.PCR)
  controls = Control.objects.filter(user=request.user)
  
  form = AssayForm(user=request.user, instance=assay)
  del_form = DeletionForm(value=assay.name)
  search_control_form = TextSearchForm()
  search_reagent_form = TextSearchForm()

  if 'update' in request.POST:
    form = AssayForm(request.POST, user=request.user, instance=assay)
    if form.is_valid():
      form.save()
      return redirect('assays')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=assay.name)
    if del_form.is_valid():
      assay.delete()
      return redirect('assays')
    else:
      print(del_form.errors)

  if 'search_control' in request.GET:
    search_control_form = TextSearchForm(request.GET)
    if search_control_form.is_valid():
      text_search = search_control_form.cleaned_data['text_search']
      controls = Control.objects.filter(Q(name__icontains=text_search) | Q(lot_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
    else:
      print(search_control_form.errors)

  if 'search_reagent' in request.GET:
    search_reagent_form = TextSearchForm(request.GET)
    if search_reagent_form.is_valid():
      text_search = search_reagent_form.cleaned_data['text_search']
      reagents = Reagent.objects.filter((Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search))).order_by(F('exp_date').asc(nulls_last=True))
    else:
      print(search_reagent_form.errors)
  
  context = {
    'assay': assay, 'form': form, 'del_form': del_form, 
    'search_control_form': search_control_form, 'search_reagent_form': search_reagent_form, 
    'controls': controls, 'reagents': reagents,
    }
  return render(request, 'assay/edit_assay.html', context)


@login_required(login_url='login')
def assay_through(request, pk):
  ReagentAssayFormSet = modelformset_factory(
    ReagentAssay,
    form=ReagentAssayForm,
    extra=0,
    )
  
  reagentformset = None

  try:
    assay = Assay.objects.get(user=request.user, pk=pk)
    reagents = ReagentAssay.objects.prefetch_related('reagent', 'assay').filter(assay=assay).order_by('order')
  except ObjectDoesNotExist:
    messages.error(request, "There is no assay to edit.")
    return redirect('extraction_protocols')
  
  reagentformset = ReagentAssayFormSet(queryset=reagents)

  reagents_data = zip(reagents, reagentformset)

  if request.method == "POST":
    reagentformset = ReagentAssayFormSet(request.POST)
    if reagentformset.is_valid():
      reagentformset.save()
      return redirect(request.path_info)
    else:
      print(reagentformset.errors)
      print(reagentformset.non_form_errors())
        
  context = {'reagentformset': reagentformset, 'reagents_data': reagents_data, 'assay': assay}
  return render(request, 'assay/assay_through.html', context)


@login_required(login_url='login')
def fluorescence(request):
  fluorescence = Fluorescence.objects.filter(user=request.user).order_by('name')

  form = SearchFluorescenseForm()
  if request.method == "GET":
    form = SearchFluorescenseForm(request.GET)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      fluorescence  = Fluorescence.objects.filter(Q(name__icontains=text_search) | Q(assay__name__icontains=text_search)).distinct().order_by('name')

  paginator = Paginator(fluorescence, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'form': form}
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
def edit_fluorescence(request, pk):
  try:
    fluorescence = Fluorescence.objects.get(user=request.user, pk=pk)
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

  form = SearchControlForm(user=request.user)
  if request.method == "GET":
    form = SearchControlForm(request.GET, user=request.user)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      location = form.cleaned_data['location']

      filters = {}
      if location:
        filters['location'] = location
      controls = Control.objects.filter(**filters, user=request.user).filter(Q(name__icontains=text_search) | Q(lot_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
  
  paginator = Paginator(controls, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'form': form}
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
def edit_control(request, pk):
  try:
    control = Control.objects.get(user=request.user, pk=pk)
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


@login_required(login_url='login')
def control_through(request, pk):
  ControlAssayFormSet = modelformset_factory(
    ControlAssay,
    form=ControlAssayForm,
    extra=0,
  )

  controlformset = None

  try:
    assay = Assay.objects.get(user=request.user, pk=pk)
    controls = ControlAssay.objects.prefetch_related('control', 'assay').filter(assay=assay).order_by('order')
  except ObjectDoesNotExist:
    messages.error(request, "There is no control to edit.")
    return redirect('controls')
  
  controlformset = ControlAssayFormSet(queryset=controls)

  controls_data = zip(controls, controlformset)

  if request.method == "POST":
    controlformset = ControlAssayFormSet(request.POST)
    if controlformset.is_valid():
      controlformset.save()
      return redirect(request.path_info)
    else:
      print(controlformset.errors)
      print(controlformset.non_form_errors())
  
  context = {'controlformset': controlformset, 'controls_data': controls_data, 'assay': assay}
  return render(request, 'assay/control_through.html', context)