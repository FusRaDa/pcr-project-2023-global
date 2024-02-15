from django.shortcuts import render

from store.models.affiliates import Brand


def landing_page(request):
  brands = Brand.objects.all()
  context = {'brands': brands}
  return render(request, 'landing_page.html', context)


def about_page(request):
  context = {}
  return render(request, 'about_page.html', context)


def faq_page(request):
  context = {}
  return render(request, 'faq_page.html', context)


def guide_page(request):
  context = {}
  return render(request, 'guide_page.html', context)