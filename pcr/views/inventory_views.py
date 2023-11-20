from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User

from ..models.inventory import Location, Reagent, Tube, Plate
from ..forms.inventory import LocationForm, ReagentForm, TubeForm, PlateForm


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

  if request.method == "POST":
    form = LocationForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('locations')
  else:
    print(form.errors)

  context = {'form': form, 'location': location}
  return render(request, 'inventory/edit_location.html', context)


@login_required(login_url='login')
def delete_location(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no location to delete.")
    return redirect('locations')
  
  try:
    location = Location.objects.get(user=user, pk=pk)
    location.delete()
  except ObjectDoesNotExist:
    messages.error(request, "There is no location to delete.")
    return redirect('locations')

  return redirect('locations')
# **LOCATIONS VIEWS** #


# **PLATES VIEWS** #
@login_required(login_url='login')
def plates(request):
  plates = Plate.objects.filter(user=request.user)

  context = {'plates': plates}
  return render(request, 'plates.html', context)


@login_required(login_url='login')
def create_plate(request):
  context = {}
  form = PlateForm()

  if request.method == "POST":
    form = PlateForm(request.POST, user=request.user)
    if form.is_valid():
      location = form.save(commit=False)
      location.user = request.user
      location = form.save()
      return redirect('plates')
  else:
    print(form.errors)

  context = {'form': form}
  return render(request, 'create_plate.html', context)


@login_required(login_url='login')
def edit_plate(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no location to edit.")
    return redirect('locations')
  
  try:
    plate = Plate.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no locaton to edit.")
    return redirect('locations')
  
  form = PlateForm(instance=plate)

  if request.method == "POST":
    form = PlateForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('locations')
  else:
    print(form.errors)

  context = {'form': form, 'plate': plate}
  return render(request, 'inventory/edit_plate.html', context)


@login_required(login_url='login')
def delete_plate(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no plate to delete.")
    return redirect('plates')
  
  try:
    plate = Plate.objects.get(user=user, pk=pk)
    plate.delete()
  except ObjectDoesNotExist:
    messages.error(request, "There is no plate to delete.")
    return redirect('plates')

  return redirect('plates')
# **PLATES VIEWS** #


# **TUBES VIEWS** #
@login_required(login_url='login')
def tubes(request):
  tubes = Tube.objects.filter(user=request.user)

  context = {'tubes': tubes}
  return render(request, 'tubes.html', context)


@login_required(login_url='login')
def create_tube(request):
  context = {}
  form = TubeForm()

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
    messages.error(request, "There is no location to edit.")
    return redirect('locations')
  
  try:
    tube = Tube.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no locaton to edit.")
    return redirect('locations')
  
  form = PlateForm(instance=tube)

  if request.method == "POST":
    form = PlateForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('locations')
  else:
    print(form.errors)

  context = {'form': form, 'tube': tube}
  return render(request, 'inventory/edit_plate.html', context)


@login_required(login_url='login')
def delete_tube(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no plate to delete.")
    return redirect('plates')
  
  try:
    tube = Tube.objects.get(user=user, pk=pk)
    tube.delete()
  except ObjectDoesNotExist:
    messages.error(request, "There is no plate to delete.")
    return redirect('plates')

  return redirect('plates')
# **TUBES VIEWS** #


# **REAGENTS VIEWS** #
@login_required(login_url='login')
def reagents(request):
  reagents = Reagent.objects.filter(user=request.user)

  context = {'reagents': reagents}
  return render(request, 'reagents.html', context)


@login_required(login_url='login')
def create_reagent(request):
  context = {}
  form = ReagentForm()

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
  
  form = ReagentForm(instance=reagent)

  if request.method == "POST":
    form = ReagentForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('reagents')
  else:
    print(form.errors)

  context = {'form': form, 'reagent': reagent}
  return render(request, 'inventory/edit_reagent.html', context)


@login_required(login_url='login')
def delete_reagent(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no reagent to delete.")
    return redirect('reagents')
  
  try:
    reagent = Reagent.objects.get(user=user, pk=pk)
    reagent.delete()
  except ObjectDoesNotExist:
    messages.error(request, "There is no reagent to delete.")
    return redirect('reagents')

  return redirect('reagents')
# **REAGENTS VIEWS** #