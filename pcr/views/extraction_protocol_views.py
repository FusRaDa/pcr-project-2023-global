from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import RestrictedError
from django.contrib import messages
from django.contrib.auth.models import User

from ..models.extraction import ExtractionProtocol, TubeExtraction, ReagentExtraction
from ..forms.extraction import ExtractionProtocolForm, TubeExtractionForm, ReagentExtractionForm

@login_required(login_url='login')
def extraction_protocols(request):
  extraction_protocols = ExtractionProtocol.objects.filter(user=request.user).order_by('name')

  context = {'extraction_protocols': extraction_protocols}
  return render(request, 'extraction-protocol/extraction_protocols.html', context)


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
      print(form.errors)
    
  context = {'form': form}
  return render(request, 'extraction-protocol/create_extraction_protocol.html', context)


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
  return render(request, 'extraction-protocol/edit_extraction_protocol.html', context)


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
  
  reagentformset = ReagentExtractionFormSet(queryset=reagents, prefix='reagent')
  tubeformset = TubeExtractionFormSet(queryset=tubes, prefix='tube')

  tubes_data = zip(tubes, tubeformset)
  reagents_data = zip(reagents, reagentformset)

  if request.method == 'POST':
    reagentformset = ReagentExtractionFormSet(request.POST, prefix='reagent')
    tubeformset = TubeExtractionFormSet(request.POST, prefix='tube')
    if reagentformset.is_valid() and tubeformset.is_valid():
      tubeformset.save()
      reagentformset.save()
      return redirect('extraction_protocols')
    else:
      print(reagentformset.errors)
      print(reagentformset.non_form_errors())
      print(tubeformset.errors)
      print(tubeformset.non_form_errors())

  context = {'tubeformset': tubeformset, 'reagentformset': reagentformset, 'tubes_data': tubes_data, 'reagents_data': reagents_data, 'protocol': protocol}
  return render(request, 'extraction-protocol/extraction_protocol_through.html', context)


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