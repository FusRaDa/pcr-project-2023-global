from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User

from ..models.inventory import Location, Reagent, Tube, Plate
from ..forms.inventory import LocationForm, Reagent, TubeForm, PlateForm


@login_required(login_url='login')
def locations(request):
  locations = Location.objects.filter(user=request.user)
  context = {'locations': locations}
  return render(request, 'locations.html', context)


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
  return render(request, 'create_location.html', context)


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
  return render(request, 'edit_location.html', context)


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