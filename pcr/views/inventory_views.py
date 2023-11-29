from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.models import User

from ..models.inventory import Location, Reagent, Tube, Plate
from ..forms.inventory import LocationForm, ReagentForm, TubeForm, PlateForm
from ..forms.general import DeletionForm


# **LOCATIONS VIEWS** #
@login_required(login_url='login')
def locations(request):
  locations = Location.objects.filter(user=request.user)

  context = {'locations': locations}
  return render(request, 'inventory/locations.html', context)


@login_required(login_url='login')
def create_location(request):
  context = {}
  form = LocationForm()

  if request.method == "POST":
    form = LocationForm(request.POST)
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
def edit_location(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no location to edit.")
    return redirect('locations')
  
  try:
    location = Location.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no locaton to edit.")
    return redirect('locations')
  
  form = LocationForm(instance=location)
  del_form = DeletionForm(value=location.name)
 
  if 'update' in request.POST:
    form = LocationForm(request.POST, instance=location)
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
      messages.error(request, "Invalid location name entered, please try again.")
      print(del_form.errors)
      return redirect(request.path_info)

  context = {'form': form, 'location': location, 'del_form': del_form}
  return render(request, 'inventory/edit_location.html', context)
# **LOCATIONS VIEWS** #


# **PLATES VIEWS** #
@login_required(login_url='login')
def plates(request):
  plates = Plate.objects.filter(user=request.user).order_by(F('exp_date').desc(nulls_last=True))

  context = {'plates': plates}
  return render(request, 'inventory/plates.html', context)


@login_required(login_url='login')
def create_plate(request):
  context = {}
  form = PlateForm(user=request.user)

  if request.method == "POST":
    form = PlateForm(request.POST, user=request.user)
    if form.is_valid():
      location = form.save(commit=False)
      location.user = request.user
      location = form.save()
      return redirect('plates')
    else:
      print(form.errors)
      print(form.non_field_errors)

  context = {'form': form}
  return render(request, 'inventory/create_plate.html', context)


@login_required(login_url='login')
def edit_plate(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no plate to edit.")
    return redirect('locations')
  
  try:
    plate = Plate.objects.get(user=user, pk=pk)
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
      return redirect(request.path_info)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=plate.name)
    if del_form.is_valid():
      plate.delete()
      return redirect('plates')
    else:
      messages.error(request, "Invalid plate name entered, please try again.")
      print(del_form.errors)
      return redirect(request.path_info)

  context = {'form': form, 'plate': plate, 'del_form': del_form}
  return render(request, 'inventory/edit_plate.html', context)
# **PLATES VIEWS** #


# **TUBES VIEWS** #
@login_required(login_url='login')
def tubes(request):
  tubes = Tube.objects.filter(user=request.user).order_by(F('exp_date').desc(nulls_last=True))

  context = {'tubes': tubes}
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
def edit_tube(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no tube to edit.")
    return redirect('tubes')
  
  try:
    tube = Tube.objects.get(user=user, pk=pk)
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
      messages.error(request, "Invalid tube name entered, please try again.")
      print(del_form.errors)
      return redirect(request.path_info)

  context = {'form': form, 'tube': tube, 'del_form': del_form}
  return render(request, 'inventory/edit_tube.html', context)
# **TUBES VIEWS** #


# **REAGENTS VIEWS** #
@login_required(login_url='login')
def reagents(request):
  pcr_reagents = Reagent.objects.filter(user=request.user, usage=Reagent.Usages.PCR).order_by(F('exp_date').asc(nulls_last=True))
  ext_reagents = Reagent.objects.filter(user=request.user, usage=Reagent.Usages.EXTRACTION).order_by(F('exp_date').asc(nulls_last=True))

  context = {'pcr_reagents': pcr_reagents, 'ext_reagents': ext_reagents}
  return render(request, 'inventory/reagents.html', context)


@login_required(login_url='login')
def create_reagent(request):
  context = {}
  form = ReagentForm(user=request.user)

  if request.method == "POST":
    form = ReagentForm(request.POST, user=request.user)
    if form.is_valid():
      reagent = form.save(commit=False)
      reagent.user = request.user
      reagent = form.save()
      return redirect('reagents')
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'inventory/create_reagent.html', context)


@login_required(login_url='login')
def edit_reagent(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no reagent to edit.")
    return redirect('reagents')
  
  try:
    reagent = Reagent.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no reagent to edit.")
    return redirect('reagents')
  
  form = ReagentForm(instance=reagent, user=request.user)
  del_form = DeletionForm(value=reagent.name)

  if 'update' in request.POST:
    form = ReagentForm(request.POST, user=request.user, instance=reagent)
    if form.is_valid():
      form.save()
      return redirect('reagents')
    else:
      print(form.errors)
 
  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=reagent.name)
    if del_form.is_valid():
      reagent.delete()
      return redirect('reagents')
    else:
      messages.error(request, "Invalid reagent name entered, please try again.")
      print(del_form.errors)
      return redirect(request.path_info)

  context = {'form': form, 'reagent': reagent, 'del_form': del_form}
  return render(request, 'inventory/edit_reagent.html', context)
# **REAGENTS VIEWS** #