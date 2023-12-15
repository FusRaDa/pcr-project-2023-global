from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# use in production with postgresql https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/#trigramsimilarity
from django.contrib.postgres.search import TrigramSimilarity

from users.models import User
from ..models.items import Kit
from ..models.orders import Order, KitOrder
from ..forms.orders import KitOrderForm
from ..forms.general import SearchStoreForm


@login_required(login_url='login')
def store(request):
  kits = Kit.objects.all()

  order = Order.objects.filter(user=request.user, has_ordered=False)
  if not order.exists():
    order = Order.objects.create(user=request.user, has_ordered=False)

  form = SearchStoreForm()
  if 'search' in request.POST:
    form = SearchStoreForm(request.POST)
    if form.is_valid():
      kit_name = form.cleaned_data['kit_name']
      cat_num = form.cleaned_data['cat_num']
      brands = form.cleaned_data['brands']
      tags = form.cleaned_data['tags']

      kits = Kit.objects.filter(brand=brands, tags=tags, name=kit_name, catalog_number=cat_num)

      # use in production with postgresql
      # kits = Kit.objects.annotate(similarity=TrigramSimilarity('name', kit_name)).filter(similarity__gt=0.3, brand=brands, tags=tags, name=kit_name, catalog_number=cat_num).order_by('-similarity')

  context = {'order': order, 'kits': kits}
  return render(request, 'orders/store.html', context)


@login_required(login_url='login')
def orders(request):
  orders = Order.objects.filter(user=request.user, has_ordered=True)
  context = {'orders': orders}
  return render(request, 'orders/orders.html', context)