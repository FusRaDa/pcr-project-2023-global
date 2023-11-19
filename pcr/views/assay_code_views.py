from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import RestrictedError

from ..models import *
from ..forms import *

@login_required(login_url='login')
def assay_codes(request):
  assay_codes = AssayCode.objects.filter(user=request.user).order_by('name')

  context = {'assay_codes': assay_codes}
  return render(request, 'assay-code/assay_codes.html', context)


@login_required(login_url='login')
def create_assay_code(request):
  context = {}
  form = AssayCodeForm(user=request.user)

  if request.method == "POST":
    form = AssayCodeForm(request.POST, user=request.user)
    if form.is_valid():
      assay_code = form.save(commit=False)
      assay_code.user = request.user
      assay_code = form.save()
      return redirect('assay_codes')
  else:
    print(form.errors)

  context = {'form': form}
  return render(request, 'assay-code/create_assay_code.html', context)


@login_required(login_url='login')
def edit_assay_code(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no assay code to edit.")
    return redirect('assay_codes')
  
  try:
    code = AssayCode.objects.get(user=user, pk=pk)
    assays = code.assays.all()
    assay_types = []
    for a in assays:
      assay_types.append(a.type)

  except ObjectDoesNotExist:
    messages.error(request, "There is no assay code to edit.")
    return redirect('assay_codes')
  
  form = AssayCodeForm(user=request.user, instance=code)

  if request.method == 'POST':
    form = AssayCodeForm(request.POST, user=request.user, instance=code)
    if form.is_valid():
      form.save()
      return redirect('assay_codes')
    else:
      print(form.errors)

  context = {'form': form, 'assay_types': assay_types, 'code': code}
  return render(request, 'assay-code/edit_assay_code.html', context)


@login_required(login_url='login')
def delete_assay_code(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no assay code to delete.")
    return redirect('assay_codes')
  
  try:
    code = AssayCode.objects.get(user=user, pk=pk)
    try:
      code.delete()
    except RestrictedError:
      messages.error(request, "You cannot delete this code as it is being used by your batches!")
      return redirect('edit_assay_code', username, pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no assay code to delete.")
    return redirect('assay_codes')

  return redirect('assay_codes')