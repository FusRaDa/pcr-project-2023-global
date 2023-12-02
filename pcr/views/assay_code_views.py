from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import RestrictedError
from django.contrib.auth.models import User

from ..models.assay import AssayCode
from ..forms.assay import AssayCodeForm
from ..forms.general import DeletionForm


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

      pcr_dna = form.cleaned_data['pcr_dna']
      pcr_rna = form.cleaned_data['pcr_rna']
      qpcr_dna = form.cleaned_data['qpcr_dna']
      qpcr_rna = form.cleaned_data['qpcr_rna']

      assays = pcr_dna | pcr_rna | qpcr_dna | qpcr_rna

      for assay in assays:
        assay_code.assays.add(assay)

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
  except ObjectDoesNotExist:
    messages.error(request, "There is no assay code to edit.")
    return redirect('assay_codes')
  
  form = AssayCodeForm(user=request.user, instance=code)
  del_form = DeletionForm(value=code.name)

  if 'update' in request.POST:
    form = AssayCodeForm(request.POST, user=request.user, instance=code)
    if form.is_valid():
      assay_code = form.save()

      pcr_dna = form.cleaned_data['pcr_dna']
      pcr_rna = form.cleaned_data['pcr_rna']
      qpcr_dna = form.cleaned_data['qpcr_dna']
      qpcr_rna = form.cleaned_data['qpcr_rna']

      assays = pcr_dna | pcr_rna | qpcr_dna | qpcr_rna

      assay_code.assays.clear()
      for assay in assays:
        assay_code.assays.add(assay)

      return redirect('assay_codes')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=code.name)
    if del_form.is_valid():
      code.delete()
      return redirect('assay_codes')
    else:
      messages.error(request, "Invalid assay code name entered, please try again.")
      print(del_form.errors)

  context = {'form': form, 'del_form': del_form, 'code': code}
  return render(request, 'assay-code/edit_assay_code.html', context)