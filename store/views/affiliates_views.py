from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from ..models.affiliates import Brand, Contact
from ..forms.affiliates import BrandForm, ContactForm
from ..forms.general import DeletionForm


@staff_member_required(login_url='login')
def brands(request):
  brands = Brand.objects.all()
  context = {'brands': brands}
  return render(request, 'affiliates/brands.html', context)


@staff_member_required(login_url='login')
def create_brand(request):
  form = BrandForm()
  if request.method == "POST":
    form = BrandForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('brands')

  context = {'form': form}
  return render(request, 'affiliates/create_brand.html', context)


@staff_member_required(login_url='login')
def edit_brand(request, pk):
  brand = Brand.objects.get(pk=pk)
  form = BrandForm(instance=brand)
  del_form = DeletionForm(value=brand.name)

  if 'update' in request.POST:
    form = BrandForm(request.POST, request.FILES, instance=brand)
    if form.is_valid():
      form.save()
      return redirect('brands')
    else:
      print(form.errors)
    
  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=brand.name)
    if del_form.is_valid():
      brand.delete()
      return redirect('brands')
    else:
      print(del_form.errors)
    
  context = {'form': form, 'del_form': del_form, 'brand': brand}
  return render(request, 'affiliates/edit_brand.html', context)


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
    else:
      print(form.errors)
  
  context = {'form': form}
  return render(request, 'affiliates/create_contact.html', context)


@staff_member_required(login_url='login')
def edit_contact(request, pk):
  contact = Contact.objects.get(pk=pk)
  form = ContactForm(instance=contact)

  if request.method == 'POST':
    form = ContactForm(request.POST, instance=contact)
    if form.is_valid():
      form.save()
      return redirect('contacts')
    
  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=contact.name)
    if del_form.is_valid():
      contact.delete()
      return redirect('contacts')
    else:
      print(del_form.errors)
    
  context = {'form': form, 'del_form': del_form, 'contact': contact}
  return render(request, 'affiliates/edit_contact.html', context)