from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import F
from django.db.models import Q
from django.contrib import messages


from ..custom.functions import find_mergeable_items
from ..models.assay import Control
from ..models.inventory import Location, Reagent, Tube, Plate, Gel, Ladder, Dye
from ..forms.inventory import LocationForm, ReagentForm, TubeForm, PlateForm, GelForm, LadderForm, DyeForm, MergeItemsForm
from ..forms.general import DeletionForm, SearchGelForm, SearchLadderForm, SearchPlateForm, SearchReagentForm, SearchTubeForm, SearchDyeForm


# **LOCATIONS VIEWS** #
@login_required(login_url='login')
def locations(request):
  locations = Location.objects.filter(user=request.user)

  context = {'locations': locations}
  return render(request, 'inventory/locations.html', context)


@login_required(login_url='login')
def create_location(request):
  context = {}
  form = LocationForm(user=request.user)

  if request.method == "POST":
    form = LocationForm(request.POST, user=request.user)
    if form.is_valid():
      location = form.save(commit=False)
      location.user = request.user
      location = form.save()
      return redirect('locations')
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'inventory/create_location.html', context)


@login_required(login_url='login')
def edit_location(request, pk):
  try:
    location = Location.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no locaton to edit.")
    return redirect('locations')
  
  form = LocationForm(instance=location, user=request.user)
  del_form = DeletionForm(value=location.name)
 
  if 'update' in request.POST:
    form = LocationForm(request.POST, instance=location, user=request.user)
    if form.is_valid():
      form.save()
      return redirect('locations')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=location.name)
    if del_form.is_valid():
      location.delete()
      return redirect('locations')
    else:
      print(del_form.errors)
   
  context = {'form': form, 'location': location, 'del_form': del_form}
  return render(request, 'inventory/edit_location.html', context)
# **LOCATIONS VIEWS** #


# **LADDER VIEWS** #
@login_required(login_url='login')
def ladders(request):
  ladders = Ladder.objects.filter(user=request.user).order_by(F('exp_date').asc(nulls_last=True))

  form = SearchLadderForm(user=request.user)
  if request.method == 'GET':
    form = SearchLadderForm(request.GET, user=request.user)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      location = form.cleaned_data['location']

      filters = {}
      if location:
        filters['location'] = location
      ladders = Ladder.objects.filter(user=request.user, **filters).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
    else:
      print(form.errors)

  paginator = Paginator(ladders, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'form': form}
  return render(request, 'inventory/ladders.html', context)


@login_required(login_url='login')
def create_ladder(request):
  form = LadderForm(user=request.user)

  if request.method == "POST":
    form = LadderForm(request.POST, user=request.user)
    if form.is_valid():
      ladder = form.save(commit=False)

      amount = form.cleaned_data['amount']
      threshold = form.cleaned_data['threshold']

      if threshold > 0:
        ladder.threshold_diff = amount - threshold
      else:
        ladder.threshold_diff = None
      
      ladder.user = request.user
      ladder = form.save()
      return redirect('ladders')
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'inventory/create_ladder.html', context)


@login_required(login_url='login')
def edit_ladder(request, pk):
  try:
    ladder = Ladder.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no ladder to edit.")
    return redirect('ladders')
  
  form = LadderForm(user=request.user, instance=ladder)
  del_form = DeletionForm(value=ladder.name)

  if 'update' in request.POST:
    form = LadderForm(request.POST, user=request.user, instance=ladder)
    if form.is_valid():

      amount = form.cleaned_data['amount']
      threshold = form.cleaned_data['threshold']

      if threshold > 0:
        ladder.threshold_diff = amount - threshold
      else:
        ladder.threshold_diff = None

      form.save()
      return redirect('ladders')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=ladder.name)
    if del_form.is_valid():
      ladder.delete()
      return redirect('ladders')
    else:
      print(del_form.errors)

  context = {'form': form, 'ladder': ladder, 'del_form': del_form}
  return render(request, 'inventory/edit_ladder.html', context)
# **LADDER VIEWS** #

# **GELS VIEWS** #
@login_required(login_url='login')
def gels(request):
  gels = Gel.objects.filter(user=request.user).order_by(F('exp_date').asc(nulls_last=True))

  form = SearchGelForm(user=request.user)
  if request.method == 'GET':
    form = SearchGelForm(request.GET, user=request.user)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      location = form.cleaned_data['location']
      size = form.cleaned_data['size']

      filters = {}
      if location:
        filters['location'] = location
      if size:
        filters['size'] = size
      gels = Gel.objects.filter(user=request.user, **filters).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
    else:
      print(form.errors)

  paginator = Paginator(gels, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'form': form}
  return render(request, 'inventory/gels.html', context)


@login_required(login_url='login')
def create_gel(request):
  form = GelForm(user=request.user)

  if request.method == "POST":
    form = GelForm(request.POST, user=request.user)
    if form.is_valid():
      gel = form.save(commit=False)

      amount = form.cleaned_data['amount']
      threshold = form.cleaned_data['threshold']

      if threshold > 0:
        gel.threshold_diff = amount - threshold
      else:
        gel.threshold_diff = None

      gel.user = request.user
      gel = form.save()
      return redirect('gels')
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'inventory/create_gel.html', context)


@login_required(login_url='login')
def edit_gel(request, pk):
  try:
    gel = Gel.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no gel to edit.")
    return redirect('gels')
  
  form = GelForm(user=request.user, instance=gel)
  del_form = DeletionForm(value=gel.name)

  if 'update' in request.POST:
    form = GelForm(request.POST, user=request.user, instance=gel)
    if form.is_valid():

      amount = form.cleaned_data['amount']
      threshold = form.cleaned_data['threshold']

      if threshold > 0:
        gel.threshold_diff = amount - threshold
      else:
        gel.threshold_diff = None

      form.save()
      return redirect('gels')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=gel.name)
    if del_form.is_valid():
      gel.delete()
      return redirect('gels')
    else:
      print(del_form.errors)

  context = {'form': form, 'gel': gel, 'del_form': del_form}
  return render(request, 'inventory/edit_gel.html', context)
# **GELS VIEWS** #


# **DYES VIEWS** #
@login_required(login_url='login')
def dyes(request):
  dyes = Dye.objects.filter(user=request.user).order_by(F('exp_date').asc(nulls_last=True))

  form = SearchDyeForm(user=request.user)
  if request.method == 'GET':
    form = SearchDyeForm(request.GET, user=request.user)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      location = form.cleaned_data['location']

      filters = {}
      if location:
        filters['location'] = location

      dyes = Dye.objects.filter(user=request.user, **filters).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
    else:
      print(form.errors)

  paginator = Paginator(dyes, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'form': form}
  return render(request, 'inventory/dyes.html', context)


@login_required(login_url='login')
def create_dye(request):
  form = DyeForm(user=request.user)

  if request.method == "POST":
    form = DyeForm(request.POST, user=request.user)
    if form.is_valid():
      dye = form.save(commit=False)

      amount = form.cleaned_data['amount']
      threshold = form.cleaned_data['threshold']

      if threshold > 0:
        dye.threshold_diff = amount - threshold
      else:
        dye.threshold_diff = None

      dye.user = request.user
      dye = form.save()
      return redirect('dyes')
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'inventory/create_dye.html', context)


@login_required(login_url='login')
def edit_dye(request, pk):
  try:
    dye = Dye.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no dye to edit.")
    return redirect('dyes')
  
  form = DyeForm(user=request.user, instance=dye)
  del_form = DeletionForm(value=dye.name)

  if 'update' in request.POST:
    form = DyeForm(request.POST, user=request.user, instance=dye)
    if form.is_valid():

      amount = form.cleaned_data['amount']
      threshold = form.cleaned_data['threshold']

      if threshold > 0:
        dye.threshold_diff = amount - threshold
      else:
        dye.threshold_diff = None

      form.save()
      return redirect('dyes')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=dye.name)
    if del_form.is_valid():
      dye.delete()
      return redirect('dyes')
    else:
      print(del_form.errors)

  context = {'form': form, 'dye': dye, 'del_form': del_form}
  return render(request, 'inventory/edit_dye.html', context)
# **DYES VIEWS** #


# **PLATES VIEWS** #
@login_required(login_url='login')
def plates(request):
  plates = Plate.objects.filter(user=request.user).order_by(F('exp_date').asc(nulls_last=True))

  form = SearchPlateForm(user=request.user)
  if request.method == 'GET':
    form = SearchPlateForm(request.GET, user=request.user)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      location = form.cleaned_data['location']
      size = form.cleaned_data['size']
      type = form.cleaned_data['type']

      filters = {}
      if location:
        filters['location'] = location
      if size:
        filters['size'] = size
      if type:
        filters['type'] = type

      plates = Plate.objects.filter(user=request.user, **filters).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
    else:
      print(form.errors)

  paginator = Paginator(plates, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'form': form}
  return render(request, 'inventory/plates.html', context)


@login_required(login_url='login')
def create_plate(request):
  form = PlateForm(user=request.user)

  if request.method == "POST":
    form = PlateForm(request.POST, user=request.user)
    if form.is_valid():
      plate = form.save(commit=False)

      amount = form.cleaned_data['amount']
      threshold = form.cleaned_data['threshold']

      if threshold > 0:
        plate.threshold_diff = amount - threshold
      else:
        plate.threshold_diff = None

      plate.user = request.user
      plate = form.save()
      return redirect('plates')
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'inventory/create_plate.html', context)


@login_required(login_url='login')
def edit_plate(request, pk):
  try:
    plate = Plate.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no plate to edit.")
    return redirect('plates')
  
  form = PlateForm(user=request.user, instance=plate)
  del_form = DeletionForm(value=plate.name)

  if 'update' in request.POST:
    form = PlateForm(request.POST, user=request.user, instance=plate)
    if form.is_valid():

      amount = form.cleaned_data['amount']
      threshold = form.cleaned_data['threshold']

      if threshold > 0:
        plate.threshold_diff = amount - threshold
      else:
        plate.threshold_diff = None

      form.save()
      return redirect('plates')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=plate.name)
    if del_form.is_valid():
      plate.delete()
      return redirect('plates')
    else:
      print(del_form.errors)

  context = {'form': form, 'plate': plate, 'del_form': del_form}
  return render(request, 'inventory/edit_plate.html', context)
# **PLATES VIEWS** #


# **TUBES VIEWS** #
@login_required(login_url='login')
def tubes(request):
  tubes = Tube.objects.filter(user=request.user).order_by(F('exp_date').asc(nulls_last=True))

  form = SearchTubeForm(user=request.user)
  if request.method == 'GET':
    form = SearchTubeForm(request.GET, user=request.user)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      location = form.cleaned_data['location']

      filters = {}
      if location:
        filters['location'] = location
      tubes = Tube.objects.filter(user=request.user, **filters).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
    else:
      print(form.errors)

  paginator = Paginator(tubes, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'form': form}
  return render(request, 'inventory/tubes.html', context)


@login_required(login_url='login')
def create_tube(request):
  context = {}
  form = TubeForm(user=request.user)

  if request.method == "POST":
    form = TubeForm(request.POST, user=request.user)
    if form.is_valid():
      tube = form.save(commit=False)

      amount = form.cleaned_data['amount']
      threshold = form.cleaned_data['threshold']

      if threshold > 0:
        tube.threshold_diff = amount - threshold
      else:
        tube.threshold_diff = None

      tube.user = request.user
      tube = form.save()
      return redirect('tubes')
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'inventory/create_tube.html', context)


@login_required(login_url='login')
def edit_tube(request, pk):
  try:
    tube = Tube.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no tube to edit.")
    return redirect('locations')
  
  form = TubeForm(instance=tube, user=request.user)
  del_form = DeletionForm(value=tube.name)

  if 'update' in request.POST:
    form = TubeForm(request.POST, user=request.user, instance=tube)
    if form.is_valid():

      amount = form.cleaned_data['amount']
      threshold = form.cleaned_data['threshold']

      if threshold > 0:
        tube.threshold_diff = amount - threshold
      else:
        tube.threshold_diff = None

      form.save()
      return redirect('tubes')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=tube.name)
    if del_form.is_valid():
      tube.delete()
      return redirect('tubes')
    else:
      print(del_form.errors)

  context = {'form': form, 'tube': tube, 'del_form': del_form}
  return render(request, 'inventory/edit_tube.html', context)
# **TUBES VIEWS** #


# **REAGENTS VIEWS** #
@login_required(login_url='login')
def reagents(request):
  reagents = Reagent.objects.filter(user=request.user).order_by(F('exp_date').asc(nulls_last=True))

  form = SearchReagentForm(user=request.user)
  if request.method == 'GET':
    form = SearchReagentForm(request.GET, user=request.user)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      location = form.cleaned_data['location']
      usage = form.cleaned_data['usage']
      pcr_reagent = form.cleaned_data['pcr_reagent']

      filters = {}
      if location:
        filters['location'] = location
      if usage:
        filters['usage'] = usage
      if pcr_reagent:
        filters['pcr_reagent'] = pcr_reagent
      reagents = Reagent.objects.filter(user=request.user, **filters).filter((Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search))).order_by(F('exp_date').asc(nulls_last=True))
    else:
      print(form.errors)

  paginator = Paginator(reagents, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'form': form}
  return render(request, 'inventory/reagents.html', context)


@login_required(login_url='login')
def create_reagent(request):
  context = {}
  form = ReagentForm(user=request.user)

  if request.method == "POST":
    form = ReagentForm(request.POST, user=request.user)
    if form.is_valid():
      reagent = form.save(commit=False)

      fseq = form.cleaned_data['forward_sequence']
      rseq = form.cleaned_data['reverse_sequence']
      usage = form.cleaned_data['usage']
      pcr_reagent = form.cleaned_data['pcr_reagent']

      volume = form.cleaned_data['volume']
      unit_volume = form.cleaned_data['unit_volume'] 

      threshold = form.cleaned_data['threshold']
      threshold_unit = form.cleaned_data['threshold_unit']

      if fseq:
        reagent.forward_sequence = fseq.upper()
      if rseq:
        reagent.reverse_sequence = rseq.upper()
      
      if unit_volume == Reagent.VolumeUnits.LITER:
        volume_in_microliters = volume * 1000000
      if unit_volume == Reagent.VolumeUnits.MILLILITER:
        volume_in_microliters = volume * 1000
      if unit_volume == Reagent.VolumeUnits.MICROLITER:
        volume_in_microliters = volume

      if threshold > 0:
        if threshold_unit == Reagent.VolumeUnits.LITER:
          reagent.threshold_diff = volume_in_microliters - (threshold * 1000000)
        if threshold_unit == Reagent.VolumeUnits.MILLILITER:
          reagent.threshold_diff = volume_in_microliters - (threshold * 1000)
        if threshold_unit == Reagent.VolumeUnits.MICROLITER:
          reagent.threshold_diff = volume_in_microliters - threshold
      else:
        reagent.threshold_diff = None

      reagent.user = request.user
      reagent = form.save()

      base_url = reverse('reagents')

      if pcr_reagent == Reagent.PCRReagent.PRIMER:
        query_string = urlencode({'usage': usage, 'pcr_reagent': pcr_reagent})
      else:
        query_string = urlencode({'usage': usage})
      
      url = '{}?{}'.format(base_url, query_string)

      return redirect(url)
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'inventory/create_reagent.html', context)


@login_required(login_url='login')
def edit_reagent(request, pk):
  try:
    reagent = Reagent.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no reagent to edit.")
    return redirect('reagents')
  
  form = ReagentForm(instance=reagent, user=request.user)
  del_form = DeletionForm(value=reagent.name)

  if 'update' in request.POST:
    form = ReagentForm(request.POST, user=request.user, instance=reagent)
    if form.is_valid():

      volume = form.cleaned_data['volume']
      unit_volume = form.cleaned_data['unit_volume'] 

      threshold = form.cleaned_data['threshold']
      threshold_unit = form.cleaned_data['threshold_unit']

      if reagent.forward_sequence:
        reagent.forward_sequence = reagent.forward_sequence.upper()
      if reagent.reverse_sequence:
        reagent.reverse_sequence = reagent.reverse_sequence.upper()

      if unit_volume == Reagent.VolumeUnits.LITER:
        volume_in_microliters = volume * 1000000
      if unit_volume == Reagent.VolumeUnits.MILLILITER:
        volume_in_microliters = volume * 1000
      if unit_volume == Reagent.VolumeUnits.MICROLITER:
        volume_in_microliters = volume

      if threshold > 0:
        if threshold_unit == Reagent.VolumeUnits.LITER:
          reagent.threshold_diff = volume_in_microliters - (threshold * 1000000)
        if threshold_unit == Reagent.VolumeUnits.MILLILITER:
          reagent.threshold_diff = volume_in_microliters - (threshold * 1000)
        if threshold_unit == Reagent.VolumeUnits.MICROLITER:
          reagent.threshold_diff = volume_in_microliters - threshold
      else:
        reagent.threshold_diff = None

      form.save()
      
      base_url = reverse('reagents')

      if reagent.pcr_reagent == Reagent.PCRReagent.PRIMER:
        query_string = urlencode({'usage': reagent.usage, 'pcr_reagent': Reagent.PCRReagent.PRIMER})
      else:
        query_string = urlencode({'usage': reagent.usage})

      url = '{}?{}'.format(base_url, query_string)

      return redirect(url)
    else:
      print(form.errors)
 
  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=reagent.name)
    if del_form.is_valid():
      reagent.delete()

      base_url = reverse('reagents')
      query_string = urlencode({'usage': reagent.usage})
      url = '{}?{}'.format(base_url, query_string)

      return redirect(url)
    else:
      print(del_form.errors)

  context = {'form': form, 'reagent': reagent, 'del_form': del_form}
  return render(request, 'inventory/edit_reagent.html', context)
# **REAGENTS VIEWS** #


# **MERGEABLE VIEWS** #
@login_required(login_url='login')
def mergeable_items(request):
  ladders = Ladder.objects.filter(user=request.user).order_by('catalog_number')
  dyes = Dye.objects.filter(user=request.user).order_by('catalog_number')
  plates = Plate.objects.filter(user=request.user).order_by('catalog_number')
  gels = Gel.objects.filter(user=request.user).order_by('catalog_number')
  tubes = Tube.objects.filter(user=request.user).order_by('catalog_number')
  reagents = Reagent.objects.filter(user=request.user).order_by('catalog_number')
  controls = Control.objects.filter(user=request.user).order_by('catalog_number')

  items = find_mergeable_items(
    ladders=ladders,
    dyes=dyes,
    plates=plates,
    gels=gels,
    tubes=tubes,
    reagents=reagents,
    controls=controls,
  )

  colors = ['table-primary', 'table-secondary', 'table-success', 'table-info', 'table-light', 'table-dark']
  
  mergeable_ladders = []
  if items['ladders']:
    color_index = 0
    for ladder in items['ladders']:
      ladders = Ladder.objects.filter(user=request.user, brand=ladder['brand'], catalog_number=ladder['cat'])
      mergeable_ladders.append({'sets': ladders, 'color': colors[color_index]})
      color_index += 1
      if color_index > 5:
          color_index = 0

  mergeable_dyes = []
  if items['dyes']:
    color_index = 0
    for dye in items['dyes']:
      dyes = Dye.objects.filter(user=request.user, brand=dye['brand'], catalog_number=dye['cat'])
      mergeable_dyes.append({'sets': dyes, 'color': colors[color_index]})
      color_index += 1
      if color_index > 5:
          color_index = 0
      
  mergeable_plates = []
  if items['plates']:
    color_index = 0
    for plate in items['plates']:
      plates = Plate.objects.filter(user=request.user, brand=plate['brand'], catalog_number=plate['cat'])
      mergeable_plates.append({'sets': plates, 'color': colors[color_index]})
      color_index += 1
      if color_index > 5:
          color_index = 0
  
  mergeable_gels = []
  if items['gels']:
    color_index = 0
    for gel in items['gels']:
      gels = Gel.objects.filter(user=request.user, brand=gel['brand'], catalog_number=gel['cat'])
      mergeable_gels.append({'sets': gels, 'color': colors[color_index]})
      color_index += 1
      if color_index > 5:
          color_index = 0
  
  mergeable_tubes = []
  if items['tubes']:
    color_index = 0
    for tube in items['tubes']:
      tubes = Tube.objects.filter(user=request.user, brand=tube['brand'], catalog_number=tube['cat'])
      mergeable_tubes.append({'sets': tubes, 'color': colors[color_index]})
      color_index += 1
      if color_index > 5:
          color_index = 0

  mergeable_reagents = []
  if items['reagents']:
    color_index = 0
    for reagent in items['reagents']:
      reagents = Reagent.objects.filter(user=request.user, brand=reagent['brand'], catalog_number=reagent['cat'])
      mergeable_reagents.append({'sets': reagents, 'color': colors[color_index]})
      color_index += 1
      if color_index > 5:
          color_index = 0

  mergeable_controls = []
  if items['controls']:
    color_index = 0
    for control in items['controls']:
      controls = Control.objects.filter(user=request.user, brand=control['brand'], catalog_number=control['cat'])
      mergeable_controls.append({'sets': controls, 'color': colors[color_index]})
      color_index += 1
      if color_index > 5:
          color_index = 0

  context = {'mergeable_ladders': mergeable_ladders, 'mergeable_dyes': mergeable_dyes, 'mergeable_plates': mergeable_plates, 'mergeable_gels': mergeable_gels, 'mergeable_tubes': mergeable_tubes, 'mergeable_reagents': mergeable_reagents, 'mergeable_controls': mergeable_controls}
  return render(request, 'inventory/mergeable_items.html', context)


@login_required(login_url='login')
def merge_ladder(request, pk):
  try:
    ladder = Ladder.objects.get(user=request.user, pk=pk)

    ladders = Ladder.objects.filter(user=request.user, catalog_number=ladder.catalog_number).exclude(pk=ladder.pk)
    if not ladders.count() > 0:
      messages.error(request, "There is no ladder to merge.")
      return redirect('inventory_report')

    form = MergeItemsForm(value=ladder.lot_number, mergeable_items=ladders)
    if 'merge' in request.POST:
      form = MergeItemsForm(request.POST, value=ladder.lot_number, mergeable_items=ladders)
      if form.is_valid():
        mergeable_items = form.cleaned_data['mergeable_items']

        lot_numbers = []
        total_amount = 0
        for obj in mergeable_items:
          total_amount += obj.amount
          lot_numbers.append(obj.lot_number)
          obj.delete()
        
        ladder.amount += total_amount
        ladder.merged_lot_numbers.extend(lot_numbers)
        ladder.save()

        return redirect('mergeable_items')
      else:
        print(form.errors)

  except ObjectDoesNotExist:
    messages.error(request, "There is no ladder to merge.")
    return redirect('inventory_report')
  
  context = {'ladder': ladder, 'form': form}
  return render(request, 'inventory/merge_ladder.html', context)


@login_required(login_url='login')
def merge_dye(request, pk):
  try:
    dye = Dye.objects.get(user=request.user, pk=pk)

    dyes = Dye.objects.filter(user=request.user, catalog_number=dye.catalog_number).exclude(pk=dye.pk)
    if not dyes.count() > 0:
      messages.error(request, "There is no dye to merge.")
      return redirect('inventory_report')
    
    form = MergeItemsForm(value=dye.lot_number, mergeable_items=dyes)
    if 'merge' in request.POST:
      form = MergeItemsForm(request.POST, value=dye.lot_number, mergeable_items=dyes)
      if form.is_valid():
        mergeable_items = form.cleaned_data['mergeable_items']

        lot_numbers = []
        total_amount = 0
        for obj in mergeable_items:
          total_amount += obj.amount
          lot_numbers.append(obj.lot_number)
          obj.delete()
        
        dye.amount += total_amount
        dye.merged_lot_numbers.extend(lot_numbers)
        dye.save()

        return redirect('mergeable_items')
      else:
        print(form.errors)

  except ObjectDoesNotExist:
    messages.error(request, "There is no dye to merge.")
    return redirect('inventory_report')
  
  context = {}
  return render(request, 'inventory/merge_dye.html', context)


@login_required(login_url='login')
def merge_plate(request, pk):
  try:
    plate = Plate.objects.get(user=request.user, pk=pk)

    plates = Plate.objects.filter(user=request.user, catalog_number=plate.catalog_number).exclude(pk=plate.pk)
    if not plates.count() > 0:
      messages.error(request, "There is no plate to merge.")
      return redirect('inventory_report')

    form = MergeItemsForm(value=plate.lot_number, mergeable_items=plates)
    if 'merge' in request.POST:
      form = MergeItemsForm(request.POST, value=plate.lot_number, mergeable_items=plates)
      if form.is_valid():
        mergeable_items = form.cleaned_data['mergeable_items']

        lot_numbers = []
        total_amount = 0
        for obj in mergeable_items:
          total_amount += obj.amount
          lot_numbers.append(obj.lot_number)
          obj.delete()
        
        plate.amount += total_amount
        plate.merged_lot_numbers.extend(lot_numbers)
        plate.save()

        return redirect('mergeable_items')
      else:
        print(form.errors)

  except ObjectDoesNotExist:
    messages.error(request, "There is no plate to merge.")
    return redirect('inventory_report')
  
  context = {'form': form, 'plate': plate, 'plates': plates}
  return render(request, 'inventory/merge_plate.html', context)


@login_required(login_url='login')
def merge_gel(request, pk):
  try:
    gel = Gel.objects.get(user=request.user, pk=pk)

    gels = Gel.objects.filter(user=request.user, catalog_number=gel.catalog_number).exclude(pk=gel.pk)
    if not gels.count() > 0:
      messages.error(request, "There is no gel to merge.")
      return redirect('inventory_report')
    
    form = MergeItemsForm(value=gel.lot_number, mergeable_items=gels)
    if 'merge' in request.POST:
      form = MergeItemsForm(request.POST, value=gel.lot_number, mergeable_items=gels)
      if form.is_valid():
        mergeable_items = form.cleaned_data['mergeable_items']

        lot_numbers = []
        total_amount = 0
        for obj in mergeable_items:
          total_amount += obj.amount
          lot_numbers.append(obj.lot_number)
          obj.delete()
        
        gel.amount += total_amount
        gel.merged_lot_numbers.extend(lot_numbers)
        gel.save()

        return redirect('mergeable_items')
      else:
        print(form.errors)

  except ObjectDoesNotExist:
    messages.error(request, "There is no gel to merge.")
    return redirect('inventory_report')

  context = {}
  return render(request, 'inventory/merge_gel.html', context)


@login_required(login_url='login')
def merge_tube(request, pk):
  try:
    tube = Tube.objects.get(user=request.user, pk=pk)

    tubes = Tube.objects.filter(user=request.user, catalog_number=tube.catalog_number).exclude(pk=tube.pk)
    if not tubes.count > 0:
      messages.error(request, "There is no tube to merge.")
      return redirect('inventory_report')
    
    form = MergeItemsForm(value=tube.lot_number, mergeable_items=tubes)
    if 'merge' in request.POST:
      form = MergeItemsForm(request.POST, value=tube.lot_number, mergeable_items=tubes)
      if form.is_valid():
        mergeable_items = form.cleaned_data['mergeable_items']

        lot_numbers = []
        total_amount = 0
        for obj in mergeable_items:
          total_amount += obj.amount
          lot_numbers.append(obj.lot_number)
          obj.delete()
        
        tube.amount += total_amount
        tube.merged_lot_numbers.extend(lot_numbers)
        tube.save()

        return redirect('mergeable_items')
      else:
        print(form.errors)

  except ObjectDoesNotExist:
    messages.error(request, "There is no gel to merge.")
    return redirect('inventory_report')
  
  context = {}
  return render(request, 'inventory/merge_tube.html', context)


@login_required(login_url='login')
def merge_reagent(request, pk):
  try:
    reagent = Reagent.objects.get(user=request.user, pk=pk)

    reagents = Reagent.objects.filter(user=request.user, catalog_number=reagent.catalog_number).exclude(pk=reagent.pk)
    if not reagents.count() > 0:
      messages.error(request, "There is no reagent to merge.")
      return redirect('inventory_report')

    form = MergeItemsForm(value=reagent.lot_number, mergeable_items=reagents)
    if 'merge' in request.POST:
      form = MergeItemsForm(request.POST, value=reagent.lot_number, mergeable_items=reagents)
      if form.is_valid():
        mergeable_items = form.cleaned_data['mergeable_items']

        lot_numbers = []
        total_amount = 0
        for obj in mergeable_items:
          total_amount += obj.volume_in_microliters
          lot_numbers.append(obj.lot_number)
          obj.delete()
        
        reagent.volume = reagent.volume_in_microliters + total_amount
        reagent.unit_volume = Reagent.VolumeUnits.MICROLITER
        reagent.merged_lot_numbers.extend(lot_numbers)
        reagent.save()

        return redirect('mergeable_items')
      else:
        print(form.errors)

  except ObjectDoesNotExist:
    messages.error(request, "There is no reagent to merge.")
    return redirect('inventory_report')
  
  context = {}
  return render(request, 'inventory/merge_reagent.html', context)


@login_required(login_url='login')
def merge_control(request, pk):
  try:
    control = Control.objects.get(user=request.user, pk=pk)

    controls = Control.objects.filter(user=request.user, catalog_number=control.catalog_number).exclude(pk=control.pk)
    if not controls.count() > 0:
      messages.error(request, "There is no control to merge.")
      return redirect('inventory_report')
    
    form = MergeItemsForm(value=control.lot_number, mergeable_items=controls)
    if 'merge' in request.POST:
      form = MergeItemsForm(request.POST, value=control.lot_number, mergeable_items=controls)
      if form.is_valid():
        mergeable_items = form.cleaned_data['mergeable_items']

        lot_numbers = []
        total_amount = 0
        for obj in mergeable_items:
          total_amount += obj.amount
          lot_numbers.append(obj.lot_number)
          obj.delete()
        
        control.amount += total_amount
        control.merged_lot_numbers.extend(lot_numbers)
        control.save()

        return redirect('mergeable_items')
      else:
        print(form.errors)

  except ObjectDoesNotExist:
    messages.error(request, "There is no control to merge.")
    return redirect('inventory_report')

  context = {}
  return render(request, 'inventory/merge_control.html', context)


@login_required(login_url='login')
def remove_ladder_lot_number(request, pk, lot):
  try:
    ladder = Ladder.objects.get(user=request.user, pk=pk)

    if not len(ladder.merged_lot_numbers) > 0:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_ladder', ladder.pk)
    
    if lot in ladder.merged_lot_numbers:
      ladder.merged_lot_numbers.remove(lot)
      ladder.save()
    else:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_ladder', ladder.pk)
    
  except ObjectDoesNotExist:
    messages.error(request, "There is no lot number to remove.")
    return redirect('edit_ladder', ladder.pk)
  
  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_dye_lot_number(request, pk, lot):
  try:
    dye = Dye.objects.get(user=request.user, pk=pk)

    if not len(dye.merged_lot_numbers) > 0:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_dye', dye.pk)

    if lot in dye.merged_lot_numbers:
      dye.merged_lot_numbers.remove(lot)
      dye.save()
    else:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_dye', dye.pk)

  except ObjectDoesNotExist:
    messages.error(request, "There is no lot number to remove.")
    return redirect('edit_dye', dye.pk)
  
  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_plate_lot_number(request, pk, lot):
  try:
    plate = Plate.objects.get(user=request.user, pk=pk)

    if not len(plate.merged_lot_numbers) > 0:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_plate', plate.pk)

    if lot in plate.merged_lot_numbers:
      plate.merged_lot_numbers.remove(lot)
      plate.save()
    else:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_plate', plate.pk)

  except ObjectDoesNotExist:
    messages.error(request, "There is no lot number to remove.")
    return redirect('edit_plate', plate.pk)
  
  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_gel_lot_number(request, pk, lot):
  try:
    gel = Gel.objects.get(user=request.user, pk=pk)

    if not len(gel.merged_lot_numbers) > 0:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_gel', gel.pk)

    if lot in gel.merged_lot_numbers:
      gel.merged_lot_numbers.remove(lot)
      gel.save()
    else:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_gel', gel.pk)

  except ObjectDoesNotExist:
    messages.error(request, "There is no lot number to remove.")
    return redirect('edit_gel', gel.pk)
  
  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_tube_lot_number(request, pk, lot):
  try:
    tube = Tube.objects.get(user=request.user, pk=pk)

    if not len(tube.merged_lot_numbers) > 0:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_tube', tube.pk)

    if lot in tube.merged_lot_numbers:
      tube.merged_lot_numbers.remove(lot)
      tube.save()
    else:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_tube', tube.pk)

  except ObjectDoesNotExist:
    messages.error(request, "There is no lot number to remove.")
    return redirect('edit_tube', tube.pk)
  
  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_reagent_lot_number(request, pk, lot):
  try:
    reagent = Reagent.objects.get(user=request.user, pk=pk)

    if not len(reagent.merged_lot_numbers) > 0:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_reagent', reagent.pk)

    if lot in reagent.merged_lot_numbers:
      reagent.merged_lot_numbers.remove(lot)
      reagent.save()
    else:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_reagent', reagent.pk)

  except ObjectDoesNotExist:
    messages.error(request, "There is no lot number to remove.")
    return redirect('edit_reagent', reagent.pk)
  
  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_control_lot_number(request, pk, lot):
  try:
    control = Control.objects.get(user=request.user, pk=pk)

    if not len(control.merged_lot_numbers) > 0:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_control', control.pk)

    if lot in control.merged_lot_numbers:
      control.merged_lot_numbers.remove(lot)
      control.save()
    else:
      messages.error(request, "There is no lot number to remove.")
      return redirect('edit_control', control.pk)

  except ObjectDoesNotExist:
    messages.error(request, "There is no lot number to remove.")
    return redirect('edit_control', control.pk)
  
  return HttpResponse(status=200)
# **MERGEABLE VIEWS** #