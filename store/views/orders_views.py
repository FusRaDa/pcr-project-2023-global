from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
  kits = Kit.objects.all()

  order = Order.objects.filter(user=request.user, has_ordered=False)
  if not order.exists():
    order = Order.objects.create(user=request.user, has_ordered=False)

  brand_tag_form = SearchBrandTagForm(prefix='brand-tag-form')
  if 'search-brand-tag' in request.POST:
    brand_tag_form = SearchBrandTagForm(request.POST, prefix='brand-tag-form')
    if brand_tag_form.is_valid():
      brands = brand_tag_form.cleaned_data['brands']
      tags = brand_tag_form.cleaned_data['tags']
      kits = Kit.objects.filter(Q(brand__in=brands) | Q(tags__in=tags))
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
def orders(request):
  orders = Order.objects.filter(user=request.user, has_ordered=True)
  context = {'orders': orders}
  return render(request, 'orders/orders.html', context)