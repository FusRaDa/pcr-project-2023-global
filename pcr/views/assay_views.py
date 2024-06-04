from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
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
      assays = Assay.objects.filter(user=request.user, **filters).order_by('name')
    else:
      print(form.errors)

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
      return redirect('edit_assay', assay.pk)
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'assay/create_assay.html', context)


@login_required(login_url='login')
def edit_assay(request, pk):
  try:
    assay = Assay.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no assay to edit.")
    return redirect('assays')
  
  assay_reagents = assay.reagentassay_set.all().order_by('order')
  assay_controls = assay.controlassay_set.all().order_by('order')

  reagents = Reagent.objects.filter(user=request.user, usage=Reagent.Usages.PCR).exclude(pk__in=assay.reagents.all())
  controls = Control.objects.filter(user=request.user).exclude(pk__in=assay.controls.all())
  
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
      controls = Control.objects.filter(user=request.user).filter(Q(name__icontains=text_search) | Q(lot_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True)).exclude(pk__in=assay.controls.all())
    else:
      print(search_control_form.errors)

  if 'search_reagent' in request.GET:
    search_reagent_form = TextSearchForm(request.GET)
    if search_reagent_form.is_valid():
      text_search = search_reagent_form.cleaned_data['text_search']
      reagents = Reagent.objects.filter(user=request.user, usage=Reagent.Usages.PCR).filter((Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search))).order_by(F('exp_date').asc(nulls_last=True)).exclude(pk__in=assay.reagents.all())
    else:
      print(search_reagent_form.errors)
  
  context = {
    'assay': assay, 'form': form, 'del_form': del_form, 
    'search_control_form': search_control_form, 'search_reagent_form': search_reagent_form, 
    'assay_reagents': assay_reagents, 'assay_controls': assay_controls,
    'controls': controls, 'reagents': reagents,
    }
  return render(request, 'assay/edit_assay.html', context)


@login_required(login_url='login')
def add_control_assay(request, assay_pk, control_pk):
  try:
    assay = Assay.objects.get(user=request.user, pk=assay_pk)
    control = Control.objects.get(user=request.user, pk=control_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no control or assay found.")
    return redirect('assays')
  
  if 'add_control' in request.POST:
    if not assay.controls.contains(control):
      assay.controls.add(control)
      context = {'assay': assay, 'control': control}
      return render(request, 'assay/control_in_assay_sent.html', context)
    
  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_control_assay(request, assay_pk, control_pk):
  try:
    assay = Assay.objects.get(user=request.user, pk=assay_pk)
    control = Control.objects.get(user=request.user, pk=control_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no control or assay found.")
    return redirect('assays')
  
  if 'remove_control' in request.POST:
    if assay.controls.contains(control):
      assay.controls.remove(control)
      context = {'assay': assay, 'control': control}
      return render(request, 'assay/add_control_assay.html', context)

  return HttpResponse(status=200)


@login_required(login_url='login')
def add_reagent_assay(request, assay_pk, reagent_pk):
  try:
    assay = Assay.objects.get(user=request.user, pk=assay_pk)
    reagent = Reagent.objects.get(user=request.user, pk=reagent_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no reagent or assay found.")
    return redirect('assays')
  
  # mixture validation
  if reagent.mixture_volume_per_reaction > assay.reaction_volume:
    return HttpResponse(status=403)
  
  if 'add_reagent' in request.POST:
    if not assay.reagents.contains(reagent):
      assay.reagents.add(reagent)
    
      if reagent.pcr_reagent != Reagent.PCRReagent.WATER and reagent.pcr_reagent != Reagent.PCRReagent.POLYMERASE and reagent.pcr_reagent != Reagent.PCRReagent.MIXTURE:
        reagent_assay = ReagentAssay.objects.get(assay=assay, reagent=reagent)
        reagent_assay.final_concentration_unit = reagent.unit_concentration
        reagent_assay.save()

      if reagent.pcr_reagent == Reagent.PCRReagent.POLYMERASE:
        reagent_assay = ReagentAssay.objects.get(assay=assay, reagent=reagent)
        reagent_assay.final_concentration_unit = "U"
        reagent_assay.save()

      context = {'assay': assay, 'reagent': reagent}
      return render(request, 'assay/reagent_in_assay_sent.html', context)

  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_reagent_assay(request, assay_pk, reagent_pk):
  try:
    assay = Assay.objects.get(user=request.user, pk=assay_pk)
    reagent = Reagent.objects.get(user=request.user, pk=reagent_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no reagent or assay found.")
    return redirect('assays')
  
  if 'remove_reagent' in request.POST:
    if assay.reagents.contains(reagent):
      assay.reagents.remove(reagent)
      context = {'assay': assay, 'reagent': reagent}
      return render(request, 'assay/add_reagent_assay.html', context)
 
  return HttpResponse(status=200)


@login_required(login_url='login')
def reagents_in_assay(request, pk):
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
  return render(request, 'assay/reagent_through.html', context)


@login_required(login_url='login')
def fluorescence(request):
  fluorescence = Fluorescence.objects.filter(user=request.user).order_by('name')

  form = SearchFluorescenseForm()
  if request.method == "GET":
    form = SearchFluorescenseForm(request.GET)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      fluorescence  = Fluorescence.objects.filter(user=request.user).filter(Q(name__icontains=text_search) | Q(assay__name__icontains=text_search)).distinct().order_by('name')
    else:
      print(form.errors)

  paginator = Paginator(fluorescence, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'form': form}
  return render(request, 'assay/fluorescence.html', context)


@login_required(login_url='login')
def create_fluorescence(request):
  context = {}
  form = FluorescenceForm(user=request.user)

  if request.method == "POST":
    form = FluorescenceForm(request.POST, user=request.user)
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
  
  form = FluorescenceForm(instance=fluorescence, user=request.user)
  del_form = DeletionForm(value=fluorescence.name)

  if 'update' in request.POST:
    form = FluorescenceForm(request.POST, instance=fluorescence, user=request.user)
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
      sort = form.cleaned_data['sort']

      filters = {}
      if location:
        filters['location'] = location
        
      if sort:
        if sort == 'exp_date' or sort == 'threshold_diff':
          controls = Control.objects.filter(user=request.user, **filters).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(F(sort).asc(nulls_last=True))
        else:
          controls = Control.objects.filter(user=request.user, **filters).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(sort)
    else:
      print(form.errors)

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
def controls_in_assay(request, pk):
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