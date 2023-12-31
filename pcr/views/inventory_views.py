from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.contrib import messages
from users.models import User

from ..models.inventory import Location, Reagent, Tube, Plate, Gel
from ..forms.inventory import LocationForm, ReagentForm, TubeForm, PlateForm, GelForm, EditGelForm, EditTubeForm, EditPlateForm, EditReagentForm
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
      print(del_form.errors)
   
  context = {'form': form, 'location': location, 'del_form': del_form}
  return render(request, 'inventory/edit_location.html', context)
# **LOCATIONS VIEWS** #


# **GELS VIEWS** #
@login_required(login_url='login')
def gels(request):
  gels = Gel.objects.filter(user=request.user).order_by(F('exp_date').desc(nulls_last=True))
  context = {'gels': gels}
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
def edit_gel(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no plate to edit.")
    return redirect('gels')
  
  try:
    gel = Gel.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no plate to edit.")
    return redirect('gels')
  
  form = EditGelForm(user=request.user, instance=gel)
  del_form = DeletionForm(value=gel.name)

  if 'update' in request.POST:
    form = EditGelForm(request.POST, user=request.user, instance=gel)
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


# **PLATES VIEWS** #
@login_required(login_url='login')
def plates(request):
  plates = Plate.objects.filter(user=request.user).order_by(F('exp_date').desc(nulls_last=True))
  context = {'plates': plates}
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
def edit_plate(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no plate to edit.")
    return redirect('plates')
  
  try:
    plate = Plate.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no plate to edit.")
    return redirect('plates')
  
  form = EditPlateForm(user=request.user, instance=plate)
  del_form = DeletionForm(value=plate.name)

  if 'update' in request.POST:
    form = EditPlateForm(request.POST, user=request.user, instance=plate)
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
  
  form = EditTubeForm(instance=tube, user=request.user)
  del_form = DeletionForm(value=tube.name)

  if 'update' in request.POST:
    form = EditTubeForm(request.POST, user=request.user, instance=tube)
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
  
  form = EditReagentForm(instance=reagent, user=request.user)
  del_form = DeletionForm(value=reagent.name)

  if 'update' in request.POST:
    form = EditReagentForm(request.POST, user=request.user, instance=reagent)
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
      print(del_form.errors)

  context = {'form': form, 'reagent': reagent, 'del_form': del_form}
  return render(request, 'inventory/edit_reagent.html', context)
# **REAGENTS VIEWS** #