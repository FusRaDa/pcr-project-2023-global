from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models import F
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse

from ..models.inventory import Reagent, Tube
from ..models.extraction import ExtractionProtocol, TubeExtraction, ReagentExtraction
from ..forms.extraction import ExtractionProtocolForm, TubeExtractionForm, ReagentExtractionForm
from ..forms.general import DeletionForm, SearchExtractionProtocolForm, TextSearchForm


@login_required(login_url='login')
def extraction_protocols(request):
  protocols = ExtractionProtocol.objects.filter(user=request.user).order_by('type')

  form = SearchExtractionProtocolForm()
  if request.method == "GET":
    form = SearchExtractionProtocolForm(request.GET)
    if form.is_valid():
      text_search = form.cleaned_data['text_search']
      type = form.cleaned_data['type']

      filters = {}
      if type:
        filters['type'] = type
      protocols = ExtractionProtocol.objects.filter(**filters, user=request.user).filter(Q(name__icontains=text_search) | Q(tubes__name__icontains=text_search) | Q(reagents__name__icontains=text_search)).distinct().order_by('name')

  paginator = Paginator(protocols, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  
  context = {'page_obj': page_obj, 'form': form}
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
      protocol.save()
      return redirect('edit_extraction_protocol', protocol.pk)
    else:
      print(form.errors)
    
  context = {'form': form}
  return render(request, 'extraction-protocol/create_extraction_protocol.html', context)


@login_required(login_url='login')
def edit_extraction_protocol(request, pk):
  try:
    protocol = ExtractionProtocol.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no extraction protocol to edit.")
    return redirect('extraction_protocols')
  
  reagents = Reagent.objects.filter(user=request.user, usage=Reagent.Usages.EXTRACTION).exclude(pk__in=protocol.reagents.all())
  tubes = Tube.objects.filter(user=request.user).exclude(pk__in=protocol.tubes.all())
  
  form = ExtractionProtocolForm(instance=protocol, user=request.user)
  del_form = DeletionForm(value=protocol.name)
  search_tube_form = TextSearchForm()
  search_reagent_form = TextSearchForm()

  if 'update' in request.POST:
    form = ExtractionProtocolForm(request.POST, instance=protocol, user=request.user)
    if form.is_valid():
      form.save()
      return redirect('extraction_protocols')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=protocol.name)
    if del_form.is_valid():
      protocol.delete()
      return redirect('extraction_protocols')
    else:
      print(del_form.errors)

  if 'search_tube' in request.GET:
    search_tube_form = TextSearchForm(request.GET)
    if search_tube_form.is_valid():
      text_search = search_tube_form.cleaned_data['text_search']
      tubes = Tube.objects.filter(user=request.user).filter((Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search))).order_by(F('exp_date').asc(nulls_last=True)).exclude(pk__in=protocol.tubes.all())
    else:
      print(search_tube_form.errors)

  if 'search_reagent' in request.GET:
    search_reagent_form = TextSearchForm(request.GET)
    if search_reagent_form.is_valid():
      text_search = search_reagent_form.cleaned_data['text_search']
      reagents = Reagent.objects.filter(user=request.user, usage=Reagent.Usages.EXTRACTION).filter((Q(name__icontains=text_search) | Q(brand__icontains=text_search) | Q(lot_number__icontains=text_search) | Q(catalog_number__icontains=text_search))).order_by(F('exp_date').asc(nulls_last=True)).exclude(pk__in=protocol.reagents.all())
    else:
      print(search_reagent_form.errors)
     
  context = {
    'form': form, 'protocol': protocol, 'del_form': del_form,
    'tubes': tubes, 'reagents': reagents, 'search_tube_form': search_tube_form,
    'search_reagent_form': search_reagent_form,
    }
  return render(request, 'extraction-protocol/edit_extraction_protocol.html', context)


@login_required(login_url='login')
def add_tube_extraction(request, protocol_pk, tube_pk):
  try:
    protocol = ExtractionProtocol.objects.get(user=request.user, pk=protocol_pk)
    tube = Tube.objects.get(user=request.user, pk=tube_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no protocol or tube found.")
    return redirect('extraction_protocols')
  
  if 'add_tube' in request.POST:
    if not protocol.tubes.contains(tube):
      protocol.tubes.add(tube)
      context = {'protocol': protocol, 'tube': tube}
      return render(request, 'extraction-protocol/tube_in_extraction.html', context)

  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_tube_extraction(request, protocol_pk, tube_pk):
  try:
    protocol = ExtractionProtocol.objects.get(user=request.user, pk=protocol_pk)
    tube = Tube.objects.get(user=request.user, pk=tube_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no protocol or tube found.")
    return redirect('extraction_protocols')
  
  if 'remove_tube' in request.POST:
    if protocol.tubes.contains(tube):
      protocol.tubes.remove(tube)
      context = {'protocol': protocol, 'tube': tube}
      return render(request, 'extraction-protocol/add_tube_extraction.html', context)

  return HttpResponse(status=200)


@login_required(login_url='login')
def add_reagent_extraction(request, protocol_pk, reagent_pk):
  try:
    protocol = ExtractionProtocol.objects.get(user=request.user, pk=protocol_pk)
    reagent = Reagent.objects.get(user=request.user, pk=reagent_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no protocol or reagent found.")
    return redirect('extraction_protocols')
  
  if 'add_reagent' in request.POST:
    if not protocol.reagents.contains(reagent):
      protocol.reagents.add(reagent)
      context = {'protocol': protocol, 'reagent': reagent}
      return render(request, 'extraction-protocol/reagent_in_extraction.html', context)
    
  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_reagent_extraction(request, protocol_pk, reagent_pk):
  try:
    protocol = ExtractionProtocol.objects.get(user=request.user, pk=protocol_pk)
    reagent = Reagent.objects.get(user=request.user, pk=reagent_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no protocol or reagent found.")
    return redirect('extraction_protocols')
  
  if 'remove_reagent' in request.POST:
    if protocol.reagents.contains(reagent):
      protocol.reagents.remove(reagent)
      context = {'protocol': protocol, 'reagent': reagent}
      return render(request, 'extraction-protocol/add_reagent_extraction.html', context)

  return HttpResponse(status=200)


@login_required(login_url='login')
def tubes_in_extraction(request, pk):
  try:
    protocol = ExtractionProtocol.objects.get(user=request.user, pk=pk)
    tubes = TubeExtraction.objects.prefetch_related('tube', 'protocol').filter(protocol=protocol).order_by('order')
  except ObjectDoesNotExist:
    messages.error(request, "There is no extraction protocol to edit.")
    return redirect('extraction_protocols')
  
  TubeExtractionFormSet = modelformset_factory(
    TubeExtraction,
    form=TubeExtractionForm,
    extra=0,
    )
  
  tubeformset = TubeExtractionFormSet(queryset=tubes)
  tubes_data = zip(tubes, tubeformset)

  if request.method == 'POST':
    tubeformset = TubeExtractionFormSet(request.POST)
    if tubeformset.is_valid():
      tubeformset.save()
      return redirect(request.path_info)
    else:
      print(tubeformset.errors)
      print(tubeformset.non_form_errors())

  context = {'tubeformset': tubeformset, 'tubes_data': tubes_data, 'protocol': protocol}
  return render(request, 'extraction-protocol/tube_through.html', context)


@login_required(login_url='login')
def reagents_in_extraction(request, pk):
  try:
    protocol = ExtractionProtocol.objects.get(user=request.user, pk=pk)
    reagents = ReagentExtraction.objects.prefetch_related('reagent', 'protocol').filter(protocol=protocol).order_by('order')
  except ObjectDoesNotExist:
    messages.error(request, "There is no extraction protocol to edit.")
    return redirect('extraction_protocols')
  
  ReagentExtractionFormSet = modelformset_factory(
    ReagentExtraction,
    form=ReagentExtractionForm,
    extra=0,
    )
  
  reagentformset = ReagentExtractionFormSet(queryset=reagents)
  reagents_data = zip(reagents, reagentformset)

  if request.method == 'POST':
    reagentformset = ReagentExtractionFormSet(request.POST)
    if reagentformset.is_valid():
      reagentformset.save()
      return redirect(request.path_info)
    else:
      print(reagentformset.errors)
      print(reagentformset.non_form_errors())

  context = {'reagentformset': reagentformset, 'reagents_data': reagents_data, 'protocol': protocol}
  return render(request, 'extraction-protocol/reagent_through.html', context)

  

@login_required(login_url='login')
def extraction_protocol_through(request, pk):
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

  try:
    protocol = ExtractionProtocol.objects.get(user=request.user, pk=pk)
    tubes = TubeExtraction.objects.prefetch_related('tube', 'protocol').filter(protocol=protocol).order_by('order')
    reagents = ReagentExtraction.objects.prefetch_related('reagent', 'protocol').filter(protocol=protocol).order_by('order')
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
      return redirect(request.path_info)
    else:
      print(reagentformset.errors)
      print(reagentformset.non_form_errors())
      print(tubeformset.errors)
      print(tubeformset.non_form_errors())

  context = {'tubeformset': tubeformset, 'reagentformset': reagentformset, 'tubes_data': tubes_data, 'reagents_data': reagents_data, 'protocol': protocol}
  return render(request, 'extraction-protocol/extraction_protocol_through.html', context)