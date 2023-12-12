from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from ..forms.affiliates import BrandForm, ContactForm

@staff_member_required(login_url='login')
def create_brand(request):

  form = BrandForm()



  context = {}
  return render(request, 'affiliates/create_brand.html', context)