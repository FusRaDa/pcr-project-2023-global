from django.shortcuts import render

from store.models.affiliates import Brand
from .forms import ContactForm


def landing_page(request):
  brands = Brand.objects.all()
  context = {'brands': brands}
  return render(request, 'landing_page.html', context)


def about_page(request):
  context = {}
  return render(request, 'about_page.html', context)