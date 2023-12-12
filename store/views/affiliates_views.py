from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from ..models.affiliates import Brand, Contact
from ..forms.affiliates import BrandForm, ContactForm


@staff_member_required(login_url='login')
def brands(request):
  brands = Brand.objects.all()
  context = {'brands': brands}
  return render(request, 'affiliates/brands.html', context)


@staff_member_required(login_url='login')
def create_brand(request):
  form = BrandForm()
  if request.method == "POST":
    form = BrandForm(request.POST)
    if form.is_valid():
      form.save()

  context = {'form': form}
  return render(request, 'affiliates/create_brand.html', context)


@staff_member_required(login_url='login')
def contacts(request):
  contacts = Contact.objects.all()
  context = {'contacts': contacts}
  return render(request, 'affiliates/contacts.html', context)


@staff_member_required(login_url='login')
def create_contact(request):
  form = ContactForm()
  if request.method == "POST":
    form = ContactForm(request.POST)
    if form.is_valid():
      form.save()
  
  context = {'form': form}
  return render(request, 'affiliates/create_contact.html', context)