from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import modelformset_factory, formset_factory

from django.core.paginator import Paginator
from datetime import datetime
from django.utils import timezone

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Q

# use in production with postgresql https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/#trigramsimilarity
from django.contrib.postgres.search import TrigramSimilarity

from ..custom.functions import generate_order_files, kit_to_inventory

from users.models import User
from ..models.items import Kit
from ..models.orders import Order, KitOrder
from ..forms.orders import KitOrderForm
from ..forms.general import SearchStoreForm, ItemLotNumberForm
from pcr.models.inventory import Plate, Tube, Reagent


@login_required(login_url='login')
def store(request):
  orders = Order.objects.filter(user=request.user, has_ordered=False)
  if not orders.exists():
    order = Order.objects.create(user=request.user, has_ordered=False)
  else:
    order = Order.objects.get(user=request.user, has_ordered=False)

  kits = Kit.objects.all().exclude(pk__in=order.kits.all()).order_by('name')

  form = SearchStoreForm()
  if request.method == 'GET':
    form = SearchStoreForm(request.GET)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      brands = form.cleaned_data['brands']
      tags = form.cleaned_data['tags']
      price = form.cleaned_data['price']

      filters = {}
      if brands:
        filters['brand__in'] = brands
      if tags:
        filters['tags__in'] = tags

      if not price:
        kits = Kit.objects.filter(**filters).filter(Q(name__icontains=text_search) | Q(description__icontains=text_search) | Q(catalog_number__icontains=text_search)).exclude(pk__in=order.kits.all()).order_by('name')
      else:
        kits = Kit.objects.filter(**filters).filter(Q(name__icontains=text_search) | Q(description__icontains=text_search) | Q(catalog_number__icontains=text_search)).exclude(pk__in=order.kits.all()).order_by(price)
  
    else:
      print(form.errors)

  paginator = Paginator(kits, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'order': order, 'page_obj': page_obj, 'form': form}
  return render(request, 'orders/store.html', context)


@login_required(login_url='login')
def add_kit_to_order(request, order_pk, kit_pk):
  try:
    order = Order.objects.get(user=request.user, pk=order_pk, has_ordered=False)
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
def remove_kit_from_order(request, order_pk, kit_pk):
  try:
    order = Order.objects.get(user=request.user, pk=order_pk, has_ordered=False)
  except ObjectDoesNotExist:
    messages.error(request, "There is no order to edit.")
    return redirect('store')
  
  if 'remove' in request.POST:
    kit = Kit.objects.get(pk=kit_pk)
    order.kits.remove(kit)

    context = {'kit': kit, 'order': order}
    return render(request, 'partials/kit_display.html', context)
  
  return HttpResponse(status=200)


@login_required(login_url='login')
def review_order(request, pk):
  try:
    order = Order.objects.get(user=request.user, has_ordered=False, pk=pk)
    order_kits = order.kits.all()
    kits = order.kitorder_set.all()
  except ObjectDoesNotExist:
    messages.error(request, "There is no order to edit.")
    return redirect('store')
  
  if not order.kits.exists():
    messages.error(request, "Please select at least one kit to add to your order.")
    return redirect('store')
  
  KitOrderFormSet = modelformset_factory(
    KitOrder,
    form=KitOrderForm,
    extra=0,
    )
  orderformset = None

  orderformset = KitOrderFormSet(queryset=kits)
  kits_data = zip(kits, orderformset)

  display_data = zip(order_kits, kits)

  if 'recalculate' in request.POST:
    orderformset = KitOrderFormSet(request.POST)
    if orderformset.is_valid():
      orderformset.save(commit=False)
      for form in orderformset:
        amount_ordered = form.cleaned_data.get('amount_ordered')
        form.instance.remaining_transfers = amount_ordered
      orderformset.save()
      return redirect(request.path_info)
    else:
      print(orderformset.errors)
      print(orderformset.non_form_errors())

  if 'process' in request.POST:
    orderformset = KitOrderFormSet(request.POST)
    if orderformset.is_valid():
      orderformset.save(commit=False)
      for form in orderformset:
        amount_ordered = form.cleaned_data.get('amount_ordered')
        form.instance.remaining_transfers = amount_ordered
      orderformset.save()
    else:
      print(orderformset.errors)
      print(orderformset.non_form_errors())

    order.has_ordered = True
    order.date_processed = timezone.now()
    order.save()

    kits_zip = order.kits.all()
    kit_orders = order.kitorder_set.all()
    zip_data = zip(kits_zip, kit_orders)

    inputs = []
    for kits_zip, kit_orders in zip_data:
      inputs.append({'brand': kits_zip.brand.name, 'catalog_number': kits_zip.catalog_number, 'amount': kit_orders.amount_ordered})
    generate_order_files(order, inputs)
    return redirect('orders')
    
  context = {'orderformset': orderformset, 'kits_data': kits_data, 'display_data': display_data, 'order': order}
  return render(request, 'orders/review_order.html', context)


@login_required(login_url='login')
def orders(request):
  orders = Order.objects.filter(user=request.user, has_ordered=True).order_by('-date_processed')
  context = {'orders': orders}
  return render(request, 'orders/orders.html', context)


@login_required(login_url='login')
def view_order(request, pk):
  try:
    order = Order.objects.get(user=request.user, has_ordered=True, pk=pk)
    kits = order.kits.all()
    kit_order = order.kitorder_set.all()
  except ObjectDoesNotExist:
    messages.error(request, "There is no order to view.")
    return redirect('orders')
  
  order_data = zip(kits, kit_order)
  
  context = {'order_data': order_data, 'order': order}
  return render(request, 'orders/view_order.html', context)


@login_required(login_url='login')
def copy_order(request, pk):
  try:
    past_order = Order.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no order to copy.")
    return redirect('orders')
  
  orders = Order.objects.filter(user=request.user, has_ordered=False)
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


@login_required(login_url='login')
def add_to_inventory(request, order_pk, kit_pk):
  try:
    order = Order.objects.get(user=request.user, pk=order_pk)
    kit = Kit.objects.get(pk=kit_pk)
    kit_order = order.kitorder_set.get(kit=kit)
  except ObjectDoesNotExist:
    messages.error(request, "There is no kit to add to your inventory.")
    return redirect('orders')
  
  if kit_order.remaining_transfers == 0:
    messages.error(request, "There is no longer any more of this kit to add from that order.")
    return redirect('orders')

  OrderFormSet = formset_factory(
    ItemLotNumberForm, 
    extra=kit_order.remaining_transfers, 
    max_num=kit_order.remaining_transfers
    )
  
  formset = OrderFormSet()

  if request.method == 'POST':
    formset = OrderFormSet(request.POST)
    if formset.is_valid():
      for form in formset:
        lot_number = form.cleaned_data.get('lot_number')
        if lot_number != None:
          kit_to_inventory(kit, request.user, lot_number)
          print('add kit...')
          kit_order.remaining_transfers -= 1
          kit_order.save()
      return redirect('view_order', order.pk)

  context = {'formset': formset, 'kit': kit, 'order': order, 'kit_order': kit_order}
  return render(request, 'orders/add_to_inventory.html', context)
  

  

