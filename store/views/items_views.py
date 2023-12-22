from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from ..models.affiliates import Brand
from ..models.items import Kit, StorePlate, StoreReagent, StoreTube, Tag, Review
from ..forms.items import KitForm, StorePlateForm, StoreReagentForm, StoreTubeForm, TagForm, ReviewForm
from ..forms.general import DeletionForm


@staff_member_required(login_url='login')
def tags(request):
  tags = Tag.objects.all()
  context = {'tags': tags}
  return render(request, 'items/tags.html', context)


@staff_member_required(login_url='login')
def create_tag(request):
  form = TagForm()

  if request.method == 'POST':
    form = TagForm(request.POST)
    if form.is_valid:
      form.save()
      return redirect('tags')

  context = {'form': form}
  return render(request, 'items/create_tag.html', context)


@staff_member_required(login_url='login')
def edit_tag(request, pk):
  tag = Tag.objects.get(pk=pk)

  form = TagForm(instance=tag)
  del_form = DeletionForm(value=tag.name)

  if 'update' in request.POST:
    form = TagForm(request.POST, instance=tag)
    if form.is_valid():
      form.save()
      return redirect('tags')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=tag.name)
    if del_form.is_valid():
      tag.delete()
      return redirect('tags')
    else:
      print(del_form.errors)

  context = {'form': form, 'del_form': del_form, 'tag': tag}
  return render(request, 'items/edit_tag.html', context)


@staff_member_required(login_url='login')
def kits(request):
  brands = Brand.objects.all()
  context = {'brands': brands}
  return render(request, 'items/kits.html', context)


@staff_member_required(login_url='login')
def create_kit(request):
  form = KitForm()

  if request.method == 'POST':
    form = KitForm(request.POST, request.FILES)
    if form.is_valid():
      kit = form.save()
      return redirect('edit_kit_items', kit.pk)
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'items/create_kit.html', context)


@staff_member_required(login_url='login')
def edit_kit(request, pk):
  kit = Kit.objects.get(pk=pk)

  form = KitForm(instance=kit)
  del_form = DeletionForm(value=kit.name)

  if 'update' in request.POST:
    form = KitForm(request.POST, request.FILES, instance=kit)
    if form.is_valid():
      form.save()
      return redirect('edit_kit_items', pk)
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
  kit = Kit.objects.get(pk=pk)
  context = {'kit': kit}
  return render(request, 'items/edit_kit_items.html', context)


@staff_member_required(login_url='login')
def create_reagent(request):
  form = StoreReagentForm()

  if request.method == 'POST':
    form = StoreReagentForm(request.POST)
    if form.is_valid():
      kit_pk = int(request.POST['pk'])
      kit = Kit.objects.get(pk=kit_pk)
      reagent = form.save(commit=False)
      reagent.kit = kit
      reagent.save()
      context = {'reagent': reagent}
      return render(request, 'partials/kit_reagents.html', context)
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'partials/store_reagent_form.html', context)


@staff_member_required(login_url='login')
def edit_reagent(request, pk):
  reagent = StoreReagent.objects.get(pk=pk)

  form = StoreReagentForm(instance=reagent)
  del_form = DeletionForm(value=reagent.name)

  if 'update' in request.POST:
    form = StoreReagentForm(request.POST, instance=reagent)
    if form.is_valid():
      form.save()
      return redirect('edit_kit_items', reagent.kit.pk)
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=reagent.name)
    if del_form.is_valid():
      reagent.delete()
      return redirect('edit_kit_items', reagent.kit.pk)
    else:
      print(del_form.errors)

  context = {'form': form, 'del_form': del_form, 'reagent': reagent}
  return render(request, 'items/edit_reagent.html', context)


@staff_member_required(login_url='login')
def create_tube(request):
  form = StoreTubeForm()
  if request.method == 'POST':
    form = StoreTubeForm(request.POST)
    if form.is_valid():
      kit_pk = int(request.POST['pk'])
      kit = Kit.objects.get(pk=kit_pk)
      tube = form.save(commit=False)
      tube.kit = kit
      tube.save()
      context = {'tube': tube}
      return render(request, 'partials/kit_tubes.html', context)
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'partials/store_tube_form.html', context)


@staff_member_required(login_url='login')
def edit_tube(request, pk):
  tube = StoreTube.objects.get(pk=pk)

  form = StoreTubeForm(instance=tube)
  del_form = DeletionForm(value=tube.name)

  if 'update' in request.POST:
    form = StoreTubeForm(request.POST, instance=tube)
    if form.is_valid():
      form.save()
      return redirect('edit_kit_items', tube.kit.pk)
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=tube.name)
    if del_form.is_valid():
      tube.delete()
      return redirect('edit_kit_items', tube.kit.pk)
    else:
      print(del_form.errors)
  
  context = {'form': form, 'del_form': del_form, 'tube': tube}
  return render(request, 'items/edit_tube.html', context)


@staff_member_required(login_url='login')
def create_plate(request):
  form = StorePlateForm()
  if request.method == 'POST':
    form = StorePlateForm(request.POST)
    if form.is_valid():
      kit_pk = int(request.POST['pk'])
      kit = Kit.objects.get(pk=kit_pk)
      plate = form.save(commit=False)
      plate.kit = kit
      plate.save()
      context = {'plate': plate}
      return render(request, 'partials/kit_plates.html', context)
    else:
      print(form.errors)
  
  context = {'form': form}
  return render(request, 'partials/store_plate_form.html', context)


@staff_member_required(login_url='login')
def edit_plate(request, pk):
  plate = StorePlate.objects.get(pk=pk)

  form = StorePlateForm(instance=plate)
  del_form = DeletionForm(value=plate.name)

  if 'update' in request.POST:
    form = StorePlateForm(request.POST, instance=plate)
    if form.is_valid():
      form.save()
      return redirect('edit_kit_items', plate.kit.pk)
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=plate.name)
    if del_form.is_valid():
      plate.delete()
      return redirect('edit_kit_items', plate.kit.pk)
    else:
      print(del_form.errors)

  context = {'form': form, 'del_form': del_form, 'plate': plate}
  return render(request, 'items/edit_plate.html', context)


@login_required(login_url='login')
def reviews(request, pk):
  form = ReviewForm()

  if request.user.can_review == False:
    messages.error(request, "You have been banned from making reviews for violating our policy. Please contact abc@gmail.com for assistance.")
    return redirect(request.path_info)
  
  kit = Kit.objects.get(pk=pk)
  reviews = Review.objects.filter(kit=kit)

  has_reviewed = False
  if Review.objects.filter(user=request.user, kit=kit).exists():
    has_reviewed = True
  
  if request.method == "POST":
    form = ReviewForm(request.POST)
    if form.is_valid():
      review = form.save(commit=False)
      review.user = request.user
      review.kit = kit
      review.save()
      return redirect(request.path_info)
    else:
      print(form.errors)

  context = {'kit': kit, 'reviews': reviews, 'has_reviewed': has_reviewed, 'form': form}
  return render(request, 'items/reviews.html', context)


  