from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import RestrictedError

from .models import *
from .forms import *
from .functions import create_samples
# Create your views here.


# **START OF SAMPLE FUNCTIONALITY** #
@login_required(login_url='login')
def viewBatches(request):

  batches = Batch.objects.filter(user=request.user).order_by('-date_created')

  context = {'batches': batches}
  return render(request, 'batches.html', context)


@login_required(login_url='login')
def createBatches(request):

  form = BatchForm(user=request.user)

  if request.method == "POST":
    form = BatchForm(request.POST, user=request.user)

    if form.is_valid():

      batch = form.save(commit=False)
      batch.user = request.user
      batch = form.save()

      number_of_samples = form.cleaned_data['number_of_samples']
      lab_id = form.cleaned_data['lab_id']

      create_samples(
        number_of_samples=number_of_samples, 
        lab_id=lab_id, 
        user=request.user,
      )

      return redirect('batch_samples', username=request.user.username, pk=batch.pk)
    
  else:
    for error in list(form.errors.values()):
      messages.error(request, error)
  
  context = {'form': form}
  return render(request, 'create_batch.html', context)


@login_required(login_url='login')
def deleteBatch(request, username, pk):

  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no batch to delete.")
    return redirect('batches')
  
  try:
    batch = Batch.objects.get(user=user, pk=pk)
    batch.delete()
  except ObjectDoesNotExist:
    messages.error(request, "There is no batch to delete.")
    return redirect('batches')

  return redirect('batches')


@login_required(login_url='login')
def batchSamples(request, username, pk):

  context = {}
  SampleFormSet = inlineformset_factory(
    Batch, 
    Sample, 
    form=SampleForm,
    extra=0, 
    can_delete=False,
    )
  formset = None

  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no batch to view.")
    return redirect('batches')
  
  try:
    batch = Batch.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no batch to view.")
    return redirect('batches')

  samples = batch.sample_set.all()
  formset = SampleFormSet(instance=batch)

  data = zip(samples, formset)

  if request.method == 'POST':
    formset = SampleFormSet(request.POST, instance=batch)
    if formset.is_valid():
      formset.save()
      return redirect('batches')
    else:
      print(formset.errors)
      print(formset.non_form_errors())
   
  context = {'batch': batch, 'data': data, 'formset': formset}
  return render(request, 'batch_samples.html', context)


@login_required(login_url='login')
def editSampleAssay(request, username, pk):

  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no sample to edit.")
    return redirect('batches')
  
  try:
    sample = Sample.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no sample to edit.")
    return redirect('batches')
  
  form = SampleAssayForm(user=request.user, instance=sample)
  
  if request.method == 'POST':
    form = SampleAssayForm(request.POST, user=request.user, instance=sample)
    if form.is_valid():
      form.save()
      return redirect('batch_samples', request.user.username, sample.batch.pk)
    else:
      print(form.errors)

  context = {'form': form}
  return render(request, 'sample_assay.html', context)
# **END OF SAMPLE FUNCTIONALITY** #


# **START OF EXTRACTION FUNCTIONALITY** #
@login_required(login_url='login')
def extraction_protocols(request):
  extraction_protocols = ExtractionProtocol.objects.filter(user=request.user)

  context = {'extraction_protocols': extraction_protocols}
  return render(request, 'extraction_protocols.html', context)


@login_required(login_url='login')
def create_extraction_protocol(request):
  context = {}
  form = ExtractionProtocolForm(user=request.user)

  if request.method == "POST":
    form = ExtractionProtocolForm(request.POST, user=request.user)
    if form.is_valid():
      protocol = form.save(commit=False)
      protocol.user = request.user
      protocol = form.save()
      return redirect('extraction_protocol_through', username=request.user.username, pk=protocol.pk)
  else:
    for error in list(form.errors.values()):
      messages.error(request, error)

  context = {'form': form}
  return render(request, 'create_extraction_protocol.html', context)


@login_required(login_url='login')
def edit_extraction_protocol(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no extraction protocol to edit.")
    return redirect('extraction_protocols')
  
  try:
    protocol = ExtractionProtocol.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no extraction protocol to edit.")
    return redirect('extraction_protocols')
  
  form = ExtractionProtocolForm(user=request.user, instance=protocol)

  if request.method == 'POST':
    form = ExtractionProtocolForm(request.POST, user=request.user, instance=protocol)
    if form.is_valid():
      form.save()
      return redirect('extraction_protocol_through', request.user.username, protocol.pk)
    else:
      print(form.errors)
  
  context = {'form': form, 'protocol': protocol}
  return render(request, 'edit_extraction_protocol.html', context)


@login_required(login_url='login')
def extraction_protocol_through(request, username, pk):
  context = {}

  TubeExtractionFormSet = modelformset_factory(
    TubeExtraction,
    form=TubeExtractionForm,
    extra=0,
    )
  
  ReagentExtractionFormSet = modelformset_factory(
    ReagentExtraction,
    form=ReagentExtractionForm,
    extra=0,
    )

  tubeformset = None
  reagentformset = None

  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no extraction protocol to edit.")
    return redirect('extraction_protocols')
  
  try:
    protocol = ExtractionProtocol.objects.get(user=user, pk=pk)
    tubes = TubeExtraction.objects.prefetch_related('tube', 'protocol').filter(protocol=protocol).order_by('-order')
    reagents = ReagentExtraction.objects.prefetch_related('reagent', 'protocol').filter(protocol=protocol).order_by('-order')
  except ObjectDoesNotExist:
    messages.error(request, "There is no extraction protocol to edit.")
    return redirect('extraction_protocols')
  
  tubeformset = TubeExtractionFormSet(queryset=tubes)
  reagentformset = ReagentExtractionFormSet(queryset=reagents)

  tubes_data = zip(tubes, tubeformset)
  reagents_data = zip(reagents, reagentformset)

  if 'tube-form' in request.POST:
    tubeformset = TubeExtractionFormSet(request.POST)
    if tubeformset.is_valid():
      tubeformset.save()
      messages.success(request, "Tube quantity and order have been modified/saved!")
      return redirect(request.path_info)
    else:
      print(tubeformset.errors)
      print(tubeformset.non_form_errors())

  if 'reagent-form' in request.POST:
    reagentformset = ReagentExtractionFormSet(request.POST)
    if reagentformset.is_valid():
      reagentformset.save()
      messages.success(request, "Reagent quantity and order have been modified/saved!")
      return redirect(request.path_info)
    else:
      print(reagentformset.errors)
      print(reagentformset.non_form_errors())

  context = {'tubeformset': tubeformset, 'reagentformset': reagentformset, 'tubes_data': tubes_data, 'reagents_data': reagents_data, 'protocol': protocol}
  return render(request, 'extraction_protocol_through.html', context)


@login_required(login_url='login')
def delete_extraction_protocol(request, username, pk):
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no extraction protocol to delete.")
    return redirect('extraction_protocols')
  
  try:
    protocol = ExtractionProtocol.objects.get(user=user, pk=pk)
    try:
      protocol.delete()
    except RestrictedError:
      messages.error(request, "You cannot delete this protocol as it is being used by your batches!")
      return redirect('edit_extraction_protocol', username, pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no extraction protocol to delete.")
    return redirect('extraction_protocols')

  return redirect('extraction_protocols')
# **START OF EXTRACTION FUNCTIONALITY** #


# **START OF ASSAY FUNCTIONALITY** #
@login_required(login_url='login')
def assay_codes(request):
  assay_codes = AssayCode.objects.filter(user=request.user)

  context = {'assay_codes': assay_codes}
  return render(request, 'assay_codes.html', context)


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
    for error in list(form.errors.values()):
      messages.error(request, error)

  context = {'form': form}
  return render(request, 'create_assay_code.html', context)


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
  return render(request, 'edit_assay_code.html', context)


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
# **END OF ASSAY FUNCTIONALITY** #



