from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from ..models.items import Kit, StorePlate, StoreReagent, StoreTube
from ..forms.items import KitForm, StorePlateForm, StoreReagentForm, StoreTubeForm
from ..forms.general import DeletionForm


def kits(request):
  kits = Kit.objects.all()
  context = {'kits': kits}
  return render(request, 'items/kits.html', context)


@staff_member_required(login_url='login')
def create_kit(request):
  form = KitForm()

  if request.method == 'POST':
    form - KitForm(request.POST)
    if form.is_valid:
      kit = form.save()
      return render(request, 'items/edit_kit_items.html', context)

  context = {'form': form}
  return render(request, 'items/create_kit.html', context)


@staff_member_required(login_url='login')
def edit_kit(request, pk):
  kit = Kit.objects.get(pk=pk)

  form = KitForm(instance=kit)
  del_form = DeletionForm(value=kit.name)

  if 'update' in request.POST:
    form = KitForm(request.POST, instance=kit)
    if form.is_valid():
      form.save()
      # return redirect('assay_through', request.user.username, pk) to items
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=kit.name)
    if del_form.is_valid():
      kit.delete()
      return redirect('kits')
    else:
      print(del_form.errors)

  context = {'form': form, 'del_form': del_form, 'kit': kit}
  return render(request, 'items/edit_kit.html', context)


@staff_member_required(login_url='login')
def edit_kit_items(request, pk):
  pass



@staff_member_required(login_url='login')
def create_tube(request):
  if request.method == 'POST':
    pass

  return render(request, 'partials/store_tube_form.html', {'form': StoreTubeForm()})


@staff_member_required(login_url='login')
def edit_tube(request, pk):
  tube = StoreTube.objects.get(pk=pk)

  form = StoreTubeForm(instance=tube)
  del_form = DeletionForm(value=tube.name)

  if 'update' in request.POST:
    form = StoreTubeForm(request.POST, instance=tube)
    if form.is_valid():
      form.save()

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=tube.name)
    if del_form.is_valid():
      tube.delete()

  return render(request, 'partials/delete_tube.html', {'del_form': del_form})


@staff_member_required(login_url='login')
def create_plate(request):
  if request.method == 'POST':
    pass

  return render(request, 'partials/store_plate_form.html', {'form': StorePlateForm()})


@staff_member_required(login_url='login')
def edit_plate(request, pk):
  plate = StorePlate.objects.get(pk=pk)

  form = StorePlateForm(instance=plate)
  del_form = DeletionForm(value=plate.name)

  if 'update' in request.POST:
    form = StorePlateForm(request.POST, instance=plate)
    if form.is_valid():
      form.save()

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=plate.name)
    if del_form.is_valid():
      plate.delete()

  return render(request, 'partials/delete_plate.html', {'del_form': del_form})


@staff_member_required(login_url='login')
def create_reagent(request):
  if request.method == 'POST':
    pass

  return render(request, 'partials/store_reagent_form.html', {'form': StoreReagentForm()})


@staff_member_required(login_url='login')
def edit_reagent(request, pk):
  reagent = StoreReagent.objects.get(pk=pk)

  form = StoreTubeForm(instance=reagent)
  del_form = DeletionForm(value=reagent.name)

  if 'update' in request.POST:
    form = StoreTubeForm(request.POST, instance=reagent)
    if form.is_valid():
      form.save()

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=reagent.name)
    if del_form.is_valid():
      reagent.delete()

  return render(request, 'partials/delete_reagent.html', {'del_form': del_form})