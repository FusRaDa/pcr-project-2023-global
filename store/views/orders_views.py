from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from datetime import datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Q

# use in production with postgresql https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/#trigramsimilarity
from django.contrib.postgres.search import TrigramSimilarity

from users.models import User
from ..models.items import Kit
from ..models.orders import Order, KitOrder
from ..forms.orders import KitOrderForm
from ..forms.general import SearchBrandTagForm, SearchCatalogForm, SearchNameForm


@login_required(login_url='login')
def store(request):

  orders = Order.objects.filter(user=request.user, has_ordered=False)
  if not orders.exists():
    order = Order.objects.create(user=request.user, has_ordered=False)
  else:
    order = Order.objects.get(user=request.user, has_ordered=False)

  kits = Kit.objects.all().order_by('name')

  brand_tag_form = SearchBrandTagForm(prefix='brand-tag-form')
  if 'search-brand-tag' in request.POST:
    brand_tag_form = SearchBrandTagForm(request.POST, prefix='brand-tag-form')
    if brand_tag_form.is_valid():
      brands = brand_tag_form.cleaned_data['brands']
      tags = brand_tag_form.cleaned_data['tags']
      if tags or brands:
        kits = Kit.objects.filter((Q(brand__in=brands) | Q(tags__in=tags)))
      if tags and brands:
        kits = Kit.objects.filter((Q(brand__in=brands) & Q(tags__in=tags)))
    else:
      print(brand_tag_form.errors)

  kit_name_form = SearchNameForm(prefix='kit-name-form')
  if 'search-kit-name' in request.POST:
    kit_name_form = SearchNameForm(request.POST, prefix='kit-name-form')
    if kit_name_form.is_valid():
      name = kit_name_form.cleaned_data['kit_name']
      kits = Kit.objects.filter(name__icontains=name)
      # use in production with postgresql
      # kits = Kit.objects.annotate(similarity=TrigramSimilarity('name', kit_name)).filter(similarity__gt=0.3).order_by('-similarity')
    else:
      print(kit_name_form.errors)

  catalog_number_form = SearchCatalogForm(prefix='catalog-number-form')
  if 'search-catalog-number' in request.POST:
    catalog_number_form = SearchCatalogForm(request.POST, prefix='catalog-number-form')
    if catalog_number_form.is_valid():
      catalog_number = catalog_number_form.cleaned_data['cat_num']
      kits = Kit.objects.filter(catalog_number__icontains=catalog_number)
    else:
      print(catalog_number_form.errors)

  context = {'order': order, 'kits': kits, 'brand_tag_form': brand_tag_form, 'kit_name_form': kit_name_form, 'catalog_number_form': catalog_number_form}
  return render(request, 'orders/store.html', context)


@login_required(login_url='login')
def add_kit_to_order(request, username, order_pk, kit_pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no order to edit.")
    return redirect('store')
  
  try:
    order = Order.objects.get(user=user, pk=order_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no order to edit.")
    return redirect('store')

  if 'add' in request.POST:
    kit = Kit.objects.get(pk=kit_pk)

    if order.kits.contains(kit):
      return HttpResponse(status=200)
    else:
      order.kits.add(kit)
      context = {'kit': kit, 'order': order}
      return render(request, 'partials/kit_order.html', context)


@login_required(login_url='login')
def remove_kit_from_order(request, username, order_pk, kit_pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no order to edit.")
    return redirect('store')
  
  try:
    order = Order.objects.get(user=user, pk=order_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no order to edit.")
    return redirect('store')
  
  if 'remove' in request.POST:
    kit = Kit.objects.get(pk=kit_pk)
    order.kits.remove(kit)

  return HttpResponse(status=200)


@login_required(login_url='login')
def review_order(request, username, pk):
  context = {}

  KitOrderFormSet = modelformset_factory(
    KitOrder,
    form=KitOrderForm,
    extra=0,
    )
  orderformset = None

  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no order to edit.")
    return redirect('store')
  
  try:
    order = Order.objects.get(user=user, pk=pk)
    order_kits = order.kits.all()
    kits = order.kitorder_set.all()
  except ObjectDoesNotExist:
    messages.error(request, "There is no order to edit.")
    return redirect('store')
  
  if not order.kits.exists():
    messages.error(request, "Please select at least one kit to add to your order.")
    return redirect('store')

  orderformset = KitOrderFormSet(queryset=kits)
  kits_data = zip(kits, orderformset)

  display_data = zip(order_kits, kits)

  if 'recalculate' in request.POST:
    orderformset = KitOrderFormSet(request.POST)
    if orderformset.is_valid():
      orderformset.save()
      return redirect(request.path_info)
    else:
      print(orderformset.errors)
      print(orderformset.non_form_errors())

  if 'process' in request.POST:
    orderformset = KitOrderFormSet(request.POST)
    if orderformset.is_valid():
      orderformset.save()
    else:
      print(orderformset.errors)
      print(orderformset.non_form_errors())

    order.has_ordered = True
    order.date_processed = datetime.now()
    order.save()
    return redirect('orders')
    # change this later for processing order
    
  context = {'orderformset': orderformset, 'kits_data': kits_data, 'display_data': display_data, 'order': order}
  return render(request, 'orders/review_order.html', context)


@login_required(login_url='login')
def orders(request):
  orders = Order.objects.filter(user=request.user, has_ordered=True).order_by('-date_processed')
  context = {'orders': orders}
  return render(request, 'orders/orders.html', context)


@login_required(login_url='login')
def view_order(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no order to view.")
    return redirect('orders')
  
  try:
    order = Order.objects.get(user=user, pk=pk)
    kits = order.kits.all()
    kit_order = order.kitorder_set.all()
    if order.has_ordered == False:
      return redirect('store')
  except ObjectDoesNotExist:
    messages.error(request, "There is no order to view.")
    return redirect('orders')
  
  order_data = zip(kits, kit_order)
  
  context = {'order_data': order_data}
  return render(request, 'orders/view_order.html', context)


@login_required(login_url='login')
def copy_order(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no order to copy.")
    return redirect('orders')
  
  try:
    past_order = Order.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no order to copy.")
    return redirect('orders')
  
  orders = Order.objects.filter(user=user, has_ordered=False)
  if not orders.exists():
    order = Order.objects.create(user=request.user, has_ordered=False)
    for kit in past_order.kits.all():
      order.kits.add(kit)
  else:
    order = Order.objects.get(user=request.user, has_ordered=False)
    order.kits.clear()
    for kit in past_order.kits.all():
      order.kits.add(kit)
  
  return redirect('store')
