from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import F
from django.db.models import Q
from django.contrib import messages
from users.models import User

from ..models.inventory import Location, Reagent, Tube, Plate, Gel, Ladder, Dye
from ..forms.inventory import LocationForm, ReagentForm, TubeForm, PlateForm, GelForm, LadderForm, DyeForm
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
      ladders = Ladder.objects.filter(**filters, user=request.user).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
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
      gels = Gel.objects.filter(**filters, user=request.user).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
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
    messages.error(request, "There is no plate to edit.")
    return redirect('gels')
  
  form = GelForm(user=request.user, instance=gel)
  del_form = DeletionForm(value=gel.name)

  if 'update' in request.POST:
    form = GelForm(request.POST, user=request.user, instance=gel)
    if form.is_valid():
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

      dyes = Dye.objects.filter(**filters, user=request.user).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
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

      plates = Plate.objects.filter(**filters, user=request.user).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
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
      tubes = Tube.objects.filter(**filters, user=request.user).filter(Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search)).order_by(F('exp_date').asc(nulls_last=True))
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
      reagents = Reagent.objects.filter(**filters, user=request.user).filter((Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search))).order_by(F('exp_date').asc(nulls_last=True))
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

      if fseq:
        reagent.forward_sequence = fseq.upper()
      if rseq:
        reagent.reverse_sequence = rseq.upper()

      reagent.user = request.user
      reagent = form.save()

      base_url = reverse('reagents')
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