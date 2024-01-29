from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator


from ..models.extraction import ExtractionProtocol, TubeExtraction, ReagentExtraction
from ..forms.extraction import ExtractionProtocolForm, TubeExtractionForm, ReagentExtractionForm
from ..forms.general import DeletionForm, SearchExtractionProtocolForm


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
      return redirect('extraction_protocols')
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
  
  form = ExtractionProtocolForm(user=request.user, instance=protocol)
  del_form = DeletionForm(value=protocol.name)

  if 'update' in request.POST:
    form = ExtractionProtocolForm(request.POST, user=request.user, instance=protocol)
    if form.is_valid():
      form.save()
      return redirect('extraction_protocols')
    else:
      print(form.errors)

  if 'update-reagents' in request.POST:
    form = ExtractionProtocolForm(request.POST, user=request.user, instance=protocol)
    if form.is_valid():
      form.save()
      return redirect('extraction_protocol_through', protocol.pk)
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=protocol.name)
    if del_form.is_valid():
      protocol.delete()
      return redirect('extraction_protocols')
    else:
      print(del_form.errors)
     
  context = {'form': form, 'protocol': protocol, 'del_form': del_form}
  return render(request, 'extraction-protocol/edit_extraction_protocol.html', context)


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