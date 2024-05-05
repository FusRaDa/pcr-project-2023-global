from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import RestrictedError
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from decimal import Decimal

from ..forms.general import DeletionForm, SearchProcessForm, SearchBatchForm
from ..forms.pcr import ThermalCyclerProtocolForm, ProcessForm
from ..models.pcr import ThermalCyclerProtocol, Process
from ..models.batch import Batch, Sample
from ..models.assay import Assay
from ..models.inventory import Reagent
from ..custom.constants import ControlThreshold
from ..custom.functions import samples_by_assay, dna_pcr_samples, rna_pcr_samples, dna_qpcr_samples, rna_qpcr_samples, process_plates, process_gels, all_pcr_samples, samples_by_assay_multiplicates


@login_required(login_url='login')
def tcprotocols(request):
  protocols = ThermalCyclerProtocol.objects.filter(user=request.user)
  context = {'protocols': protocols}
  return render(request, 'pcr/tcprotocols.html', context)


@login_required(login_url='login')
def create_tcprotocol(request):
  form = ThermalCyclerProtocolForm(user=request.user)
  
  if request.method == "POST":
    form = ThermalCyclerProtocolForm(request.POST, user=request.user)
    if form.is_valid():
      protocol = form.save(commit=False)
      protocol.user = request.user
      protocol.save()
      return redirect('tcprotocols')
    else:
      print(form.errors)
  
  context = {'form': form}
  return render(request, 'pcr/create_tcprotocol.html', context)


@login_required(login_url='login')
def edit_tcprotocol(request, pk):
  try:
    protocol = ThermalCyclerProtocol.objects.get(user=request.user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no thermal cycler protocol to edit.")
    return redirect('tcprotocols')
  
  form = ThermalCyclerProtocolForm(instance=protocol, user=request.user)
  del_form = DeletionForm(value=protocol.name)
 
  if 'update' in request.POST:
    form = ThermalCyclerProtocolForm(request.POST, instance=protocol, user=request.user)
    if form.is_valid():
      form.save()
      return redirect('tcprotocols')
    else:
      print(form.errors)

  if 'delete' in request.POST:
    del_form = DeletionForm(request.POST, value=protocol.name)
    if del_form.is_valid():
      try:
        protocol.delete()
        return redirect('tcprotocols')
      except RestrictedError:
        messages.error(request, f"{protocol.name} cannot be deleted since it is being used in a PCR process.")
        return redirect('tcprotocols')
    else:
      print(del_form.errors)

  context = {'form': form, 'del_form': del_form, 'protocol': protocol}
  return render(request, 'pcr/edit_tcprotocol.html', context)


@login_required(login_url='login')
def extracted_batches(request):
  process = Process.objects.filter(user=request.user, is_processed=False)
  if not process.exists():
    process = Process.objects.create(user=request.user)
  else:
    process = Process.objects.get(user=request.user, is_processed=False)

  batches = Batch.objects.filter(user=request.user, is_extracted=True).order_by('date_created')

  if 'clear' in request.POST:
    process.samples.clear()
    return redirect(request.path_info)
  
  form = SearchBatchForm(user=request.user)
  if request.method == "GET":
    form = SearchBatchForm(request.GET, user=request.user)
    if form.is_valid():
      name = form.cleaned_data['name']
      lab_id = form.cleaned_data['lab_id']
      panel = form.cleaned_data['panel']
      protocol = form.cleaned_data['extraction_protocol']
      start_date = form.cleaned_data['start_date']
      end_date = form.cleaned_data['end_date']

      filters = {}
      if name:
        filters['name__icontains'] = name
      if panel:
        filters['code'] = panel
      if lab_id:
        filters['lab_id'] = lab_id
      if protocol:
        filters['extraction_protocol'] = protocol
      
      if start_date and not end_date:
        day = start_date + datetime.timedelta(days=1)
        filters['date_created__range'] = [start_date, day]

      if end_date and not start_date:
        day = end_date + datetime.timedelta(days=1)
        filters['date_created__range'] = [end_date, day]
      
      if start_date and end_date:
        end_date += datetime.timedelta(days=1)
        filters['date_created__range'] = [start_date, end_date]

      batches = Batch.objects.filter(user=request.user, is_extracted=True, **filters).order_by('date_created')
    else:
      print(form.errors)

  paginator = Paginator(batches, 10)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  context = {'page_obj': page_obj, 'process': process, 'form': form}
  return render(request, 'pcr/extracted_batches.html', context)


@login_required(login_url='login')
def add_batch_samples(request, process_pk, batch_pk):
  try:
    batch = Batch.objects.get(user=request.user, pk=batch_pk)
    process = Process.objects.get(user=request.user, pk=process_pk, is_processed=False)
  except ObjectDoesNotExist:
    messages.error(request, "There is no sample or process found.")
    return redirect('extracted_batches')
  
  if 'all' in request.POST:
    added_samples = []
    samples = batch.sample_set.all()
    for sample in samples:
      if not process.samples.contains(sample):
        process.samples.add(sample)
        added_samples.append(sample)

    context = {'added_samples': added_samples, 'process': process}
    return render(request, 'pcr/batch_in_process.html', context)
      
  return HttpResponse(status=200)


@login_required(login_url='login')
def add_sample_to_process(request, process_pk, sample_pk):
  try:
    sample = Sample.objects.get(user=request.user, pk=sample_pk)
    process = Process.objects.get(user=request.user, pk=process_pk, is_processed=False)
  except ObjectDoesNotExist:
    messages.error(request, "There is no sample or process found.")
    return redirect('extracted_batches')
  
  if 'add' in request.POST:
    if not process.samples.contains(sample):
      process.samples.add(sample)
      context = {'sample': sample, 'process': process}
      return render(request, 'pcr/samples_in_process.html', context)

  return HttpResponse(status=200)


@login_required(login_url='login')
def remove_sample_from_process(request, process_pk, sample_pk):
  try:
    sample = Sample.objects.get(user=request.user, pk=sample_pk)
    process = Process.objects.get(user=request.user, is_processed=False, pk=process_pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no sample or process found.")
    return redirect('extracted_batches')
  
  if 'remove' in request.POST:
    process.samples.remove(sample)
  
  return HttpResponse(status=200)


@login_required(login_url='login')
def review_process(request, pk):
  try:
    process = Process.objects.get(user=request.user, is_processed=False, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no process to review.")
    return redirect('extracted_batches')
  
  samples = process.samples.all()
  if samples.count() < 1:
    messages.error(request, "Process must have at least one sample.")
    return redirect('extracted_batches')

  assay_samples = samples_by_assay(samples)
  
  form = ProcessForm(instance=process, user=request.user)

  if request.method == 'POST':
    form = ProcessForm(request.POST, instance=process, user=request.user)
    if form.is_valid():
      form.save()
      return redirect('process_paperwork', process.pk)
    else:
      print(form.errors)
  
  context = {'form': form, 'assay_samples': assay_samples, 'process': process}
  return render(request, 'pcr/review_process.html', context)


@login_required(login_url='login')
def process_paperwork(request, pk):
  try:
    process = Process.objects.get(user=request.user, is_processed=False, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no process to review.")
    return redirect('extracted_batches')
  
  samples = process.samples.all()
  assay_samples = samples_by_assay_multiplicates(samples)

  requires_dna_pcr = False
  requires_rna_pcr = False
  requires_dna_qpcr = False
  requires_rna_qpcr = False

  for assay in assay_samples:
    for a in assay.keys():
      if a.type == Assay.Types.DNA and a.method == Assay.Methods.PCR:
        requires_dna_pcr = True
      if a.type == Assay.Types.RNA and a.method == Assay.Methods.PCR: 
        requires_rna_pcr = True
      if a.type == Assay.Types.DNA and a.method == Assay.Methods.qPCR:
        requires_dna_qpcr = True
      if a.type == Assay.Types.RNA and a.method == Assay.Methods.qPCR:
        requires_rna_qpcr = True

  qpcr_plates = []
  for plate in process.qpcr_plate.all().order_by('size'):
    qpcr_plates.append({'plate': plate, 'name': plate.name, 'catalog_number': plate.catalog_number, 'lot_number': plate.lot_number, 'size': plate.size, 'amount': plate.amount, 'used': 0})

  pcr_plates = []
  for plate in process.pcr_plate.all().order_by('size'):
    pcr_plates.append({'plate': plate, 'name': plate.name, 'catalog_number': plate.catalog_number, 'lot_number': plate.lot_number, 'size': plate.size, 'amount': plate.amount, 'used': 0})

  gels = []
  for gel in process.gel.all().order_by('size'):
    gels.append({'gel': gel, 'name': gel.name, 'catalog_number': gel.catalog_number, 'lot_number': gel.lot_number, 'size': gel.size, 'amount': gel.amount, 'used': 0})

  reagent_usage = []
  control_usage = []

  # **GENERATE PLATES FOR qPCR** #
  dna_qpcr_json = None
  if requires_dna_qpcr:
    samples_dna_qpcr = dna_qpcr_samples(assay_samples)
    dna_qpcr_json = process_plates(samples_dna_qpcr, qpcr_plates, process.qpcr_dna_protocol, process.min_samples_per_plate_dna_qpcr, process.loading_method_qdna)

    for plate in dna_qpcr_json:
      for assay in plate['assays']:
        sample_num = assay['sample_num']
        for reagent in assay['reagents']:
          
          if process.is_plus_one_well:
            usage = round((reagent['volume_per_sample'] * (sample_num + 1)), 2)
          else:
            usage = round((reagent['volume_per_sample'] * sample_num), 2)

          exists = False
          for dict in reagent_usage:
            if dict['reagent'].pk == reagent['reagent'].pk:
              exists = True

          if exists == False:
            reagent_usage.append({'reagent': reagent['reagent'], 'usage': usage})
          else:
            for dict in reagent_usage:
              if dict['reagent'].pk == reagent['reagent'].pk:
                dict['usage'] += usage
                break

        for control in assay['controls']:
          exists = False
          for dict in control_usage:
            if dict['control'].pk == control.pk:
              exists = True
              break
          
          if exists == False:
            control_usage.append({'control': control, 'usage': assay['sample_volume']})
          else:
            for dict in control_usage:
              if dict['control'].pk == control.pk:
                dict['usage'] += assay['sample_volume']
                break
        
  rna_qpcr_json = None
  if requires_rna_qpcr:
    samples_rna_qpcr = rna_qpcr_samples(assay_samples)
    rna_qpcr_json = process_plates(samples_rna_qpcr, qpcr_plates, process.qpcr_rna_protocol, process.min_samples_per_plate_rna_qpcr, process.loading_method_qrna)

    for plate in rna_qpcr_json:
      for assay in plate['assays']:
        sample_num = assay['sample_num']
        for reagent in assay['reagents']:
          
          if process.is_plus_one_well:
            usage = round((reagent['volume_per_sample'] * (sample_num + 1)), 2)
          else:
            usage = round((reagent['volume_per_sample'] * sample_num), 2)

          exists = False
          for dict in reagent_usage:
            if dict['reagent'].pk == reagent['reagent'].pk:
              exists = True

          if exists == False:
            reagent_usage.append({'reagent': reagent['reagent'], 'usage': usage})
          else:
            for dict in reagent_usage:
              if dict['reagent'].pk == reagent['reagent'].pk:
                dict['usage'] += usage
                break

        for control in assay['controls']:
          exists = False
          for dict in control_usage:
            if dict['control'].pk == control.pk:
              exists = True
              break
          
          if exists == False:
            control_usage.append({'control': control, 'usage': assay['sample_volume']})
          else:
            for dict in control_usage:
              if dict['control'].pk == control.pk:
                dict['usage'] += assay['sample_volume']
                break
  # **GENERATE PLATES FOR qPCR** #
    
  # **GENERATE PLATES FOR PCR** #
  dna_pcr_json = None
  if requires_dna_pcr:
    samples_dna_pcr = dna_pcr_samples(assay_samples)
    dna_pcr_json = process_plates(samples_dna_pcr, pcr_plates, process.pcr_dna_protocol, process.min_samples_per_plate_dna_pcr, process.loading_method_dna)

    for plate in dna_pcr_json:
      for assay in plate['assays']:
        sample_num = assay['sample_num']
        for reagent in assay['reagents']:
          
          if process.is_plus_one_well:
            usage = round((reagent['volume_per_sample'] * (sample_num + 1)), 2)
          else:
            usage = round((reagent['volume_per_sample'] * sample_num), 2)
          
          exists = False
          for dict in reagent_usage:
            if dict['reagent'].pk == reagent['reagent'].pk:
              exists = True

          if exists == False:
            reagent_usage.append({'reagent': reagent['reagent'], 'usage': usage})
          else:
            for dict in reagent_usage:
              if dict['reagent'].pk == reagent['reagent'].pk:
                dict['usage'] += usage
                break

        for control in assay['controls']:
          exists = False
          for dict in control_usage:
            if dict['control'].pk == control.pk:
              exists = True
              break
          
          if exists == False:
            control_usage.append({'control': control, 'usage': assay['sample_volume']})
          else:
            for dict in control_usage:
              if dict['control'].pk == control.pk:
                dict['usage'] += assay['sample_volume']
                break

  rna_pcr_json = None
  if requires_rna_pcr:
    samples_rna_pcr = rna_pcr_samples(assay_samples)
    rna_pcr_json = process_plates(samples_rna_pcr, pcr_plates, process.pcr_rna_protocol, process.min_samples_per_plate_rna_pcr, process.loading_method_rna)

    for plate in rna_pcr_json:
      for assay in plate['assays']:
        sample_num = assay['sample_num']
        for reagent in assay['reagents']:
          
          if process.is_plus_one_well:
            usage = round((reagent['volume_per_sample'] * (sample_num + 1)), 2)
          else:
            usage = round((reagent['volume_per_sample'] * sample_num), 2)

          exists = False
          for dict in reagent_usage:
            if dict['reagent'].pk == reagent['reagent'].pk:
              exists = True

          if exists == False:
            reagent_usage.append({'reagent': reagent['reagent'], 'usage': usage})
          else:
            for dict in reagent_usage:
              if dict['reagent'].pk == reagent['reagent'].pk:
                dict['usage'] += usage
                break

        for control in assay['controls']:
          exists = False
          for dict in control_usage:
            if dict['control'].pk == control.pk:
              exists = True
              break
          
          if exists == False:
            control_usage.append({'control': control, 'usage': assay['sample_volume']})
          else:
            for dict in control_usage:
              if dict['control'].pk == control.pk:
                dict['usage'] += assay['sample_volume']
                break
  # **GENERATE PLATES FOR PCR** #
 
  # **GENERATE GELS FOR PCR** #
  pcr_gels_json = None
  if requires_dna_pcr or requires_rna_pcr:
    gel_samples = all_pcr_samples(assay_samples)
    pcr_gels_json = process_gels(gel_samples, gels, process.min_samples_per_gel)
  # **GENERATE GELS FOR PCR** #
  
  if 'process' in request.POST:

    # **RECOLLECT REAGENTS & CONTROLS FOR PCR & qPCR** #
    all_controls = []
    all_reagents = []
    
    if dna_qpcr_json:
      for plate in dna_qpcr_json:
        for assay in plate['assays']:

          for control in assay['controls']:
            total_volume = Decimal(assay['sample_volume'])

            exists = False
            for dict in all_controls:
              if dict['control'].pk == control.pk:
                exists = True
                break
            
            if exists == False:
              all_controls.append({'control': control, 'total': total_volume})
            else:
              for dict in all_controls:
                if dict['control'].pk == control.pk:
                  dict['total'] += total_volume
                  break
          assay.pop('controls')
            
          for reagent in assay['reagents']:
            reagent_obj = reagent['reagent']
            total_volume = Decimal(reagent['volume_per_sample'] * assay['sample_num'])
            volume_per_sample = Decimal(reagent['volume_per_sample'])

            exists = False
            for dict in all_reagents:
              if dict['reagent'].pk == reagent_obj.pk:
                exists = True
                break
            
            if exists == False:
              all_reagents.append({'reagent': reagent_obj, 'total' : total_volume, 'volume_per_sample': volume_per_sample})
            else:
              for dict in all_reagents:
                if dict['reagent'].pk == reagent_obj.pk:
                  dict['total'] += total_volume
                  break
            reagent.pop('reagent')

    if rna_qpcr_json:
      for plate in rna_qpcr_json:
        for assay in plate['assays']:

          for control in assay['controls']:
            total_volume = Decimal(assay['sample_volume'])

            exists = False
            for dict in all_controls:
              if dict['control'].pk == control.pk:
                exists = True
                break
            
            if exists == False:
              all_controls.append({'control': control, 'total': total_volume})
            else:
              for dict in all_controls:
                if dict['control'].pk == control.pk:
                  dict['total'] += total_volume
                  break
          assay.pop('controls')

          for reagent in assay['reagents']:
            reagent_obj = reagent['reagent']
            total_volume = Decimal(reagent['volume_per_sample'] * assay['sample_num'])
            volume_per_sample = Decimal(reagent['volume_per_sample'])

            exists = False
            for dict in all_reagents:
              if dict['reagent'].pk == reagent_obj.pk:
                exists = True
                break
            
            if exists == False:
              all_reagents.append({'reagent': reagent_obj, 'total' : total_volume, 'volume_per_sample': volume_per_sample})
            else:
              for dict in all_reagents:
                if dict['reagent'].pk == reagent_obj.pk:
                  dict['total'] += total_volume
                  break
            reagent.pop('reagent')

    if dna_pcr_json:
      for plate in dna_pcr_json:
        for assay in plate['assays']:

          for control in assay['controls']:
            total_volume = Decimal(assay['sample_volume'])

            exists = False
            for dict in all_controls:
              if dict['control'].pk == control.pk:
                exists = True
                break
            
            if exists == False:
              all_controls.append({'control': control, 'total': total_volume})
            else:
              for dict in all_controls:
                if dict['control'].pk == control.pk:
                  dict['total'] += total_volume
                  break
          assay.pop('controls')

          for reagent in assay['reagents']:
            reagent_obj = reagent['reagent']
            total_volume = Decimal(reagent['volume_per_sample'] * assay['sample_num'])
            volume_per_sample = Decimal(reagent['volume_per_sample'])

            exists = False
            for dict in all_reagents:
              if dict['reagent'].pk == reagent_obj.pk:
                exists = True
                break
            
            if exists == False:
              all_reagents.append({'reagent': reagent_obj, 'total' : total_volume, 'volume_per_sample': volume_per_sample})
            else:
              for dict in all_reagents:
                if dict['reagent'].pk == reagent_obj.pk:
                  dict['total'] += total_volume
                  break
            reagent.pop('reagent')

    if rna_pcr_json:
      for plate in rna_pcr_json:
        for assay in plate['assays']:

          for control in assay['controls']:
            total_volume = Decimal(assay['sample_volume'])

            exists = False
            for dict in all_controls:
              if dict['control'].pk == control.pk:
                exists = True
                break
            
            if exists == False:
              all_controls.append({'control': control, 'total': total_volume})
            else:
              for dict in all_controls:
                if dict['control'].pk == control.pk:
                  dict['total'] += total_volume
                  break
          assay.pop('controls')

          for reagent in assay['reagents']:
            reagent_obj = reagent['reagent']
            total_volume = Decimal(reagent['volume_per_sample'] * assay['sample_num'])
            volume_per_sample = Decimal(reagent['volume_per_sample'])

            exists = False
            for dict in all_reagents:
              if dict['reagent'].pk == reagent_obj.pk:
                exists = True
                break
            
            if exists == False:
              all_reagents.append({'reagent': reagent_obj, 'total' : total_volume, 'volume_per_sample': volume_per_sample})
            else:
              for dict in all_reagents:
                if dict['reagent'].pk == reagent_obj.pk:
                  dict['total'] += total_volume
                  break
            reagent.pop('reagent')
    # **RECOLLECT REAGENTS & CONTROLS FOR PCR & qPCR** #
    

    # **RECOLLECT DYES AND LADDERS ** #
    all_dyes = []
    all_ladders = []
    if pcr_gels_json:
      for gel in pcr_gels_json:
        for dye in gel['dyes']:
          dye_obj = dye['dye']
          total_volume = Decimal(dye['volume_per_well'] * dye['sample_num'])

          if dye['dye_in_ladder'] == True:
            total_volume += Decimal(dye['volume_per_well'])
            
          exists = False
          for dict in all_dyes:
            if dict['dye'].pk == dye_obj.pk:
              exists = True
              break
          
          if exists == False:
            all_dyes.append({'dye': dye_obj, 'total': total_volume})
          else:
            for dict in all_dyes:
              if dict['dye'].pk == dye_obj.pk:
                dict['total'] += total_volume
                break
          dye.pop('dye')
        
      for gel in pcr_gels_json:
        for ladder in gel['ladders']:
          ladder_obj = ladder['ladder']
          total_volume = Decimal(ladder['volume_per_gel'])

          exists = False
          for dict in all_ladders:
            if dict['ladder'].pk == ladder_obj.pk:
              exists = True
              break
          
          if exists == False:
            all_ladders.append({'ladder': ladder_obj, 'total': total_volume})
          else:
            for dict in all_ladders:
              if dict['ladder'].pk == ladder_obj.pk:
                dict['total'] += total_volume
                break
          ladder.pop('ladder')
    # **RECOLLECT DYES AND LADDERS ** #
        

    # **VALIDATION FOR PLATES & GELS** #
    for plate in qpcr_plates:
      if plate['plate'].is_expired:
        messages.error(request, f"Plate: {plate.name} lot#: {plate.lot_number} is expired.")
        return redirect(request.path_info)
      
      if plate['amount'] < 0:
        messages.error(request, f"Plate: {plate.name} lot#: {plate.lot_number} for qPCR has an insufficient amount for this process. {plate['amount']} plates are required. Please update inventory or change selection.")
        return redirect(request.path_info)
    
    for plate in pcr_plates:
      if plate['plate'].is_expired:
        messages.error(request, f"Plate: {plate.name} lot#: {plate.lot_number} is expired.")
        return redirect(request.path_info)
      
      if plate['amount'] < 0:
        messages.error(request, f"Plate: {plate.name} lot#: {plate.lot_number} for PCR has an insufficient amount for this process. {plate['amount']} plates are required. Please update inventory or change selection.")
        return redirect(request.path_info)

    for gel in gels:
      if gel['gel'].is_expired:
        messages.error(request, f"Gel: {gel.name} lot#: {gel.lot_number} is expired.")
        return redirect(request.path_info)
      
      if gel['amount'] < 0:
        messages.error(request, f"Gel: {gel.name} lot#: {gel.lot_number} has an insufficient amount for this process. {gel['amount']} gels are required. Please update inventory or change selection.")
        return redirect(request.path_info)
    # **VALIDATION FOR PLATES & GELS** #
      

    # **VALIDATION FOR CONTROLS** #
    for control_dict in all_controls:
      name = control_dict['control'].name
      lot_number = control_dict['control'].lot_number

      if control_dict['control'].is_expired:
        messages.error(request, f"Control: {name} lot#: {lot_number} is expired")
        return redirect(request.path_info)
      
      if control_dict['control'].amount - control_dict['total'] < 0:
        messages.error(request, f"Control: {name} lot#: {lot_number} has an insufficient amount for this process. {round(control_dict['total'], 2)}µl is required. Please update inventory or change selection.")
        return redirect(request.path_info)
    # **VALIDATION FOR CONTROLS** #
      
    
    # **VALIDATION FOR REAGENTS** #
    for reagent_dict in all_reagents:
      name = reagent_dict['reagent'].name
      lot_number = reagent_dict['reagent'].lot_number
      
      if reagent_dict['reagent'].is_expired:
        messages.error(request, f"Reagent: {name} lot#: {lot_number} is expired")
        return redirect(request.path_info)
      
      if reagent_dict['reagent'].volume_in_microliters - reagent_dict['total'] < 0:
        messages.error(request, f"Reagent: {name} lot#: {lot_number} has an insufficient amount for this process. {round(reagent_dict['total'], 2)}µl is required. Please update inventory or change selection.")
        return redirect(request.path_info)
    # **VALIDATION FOR REAGENTS** #
      

    # **VALIDATION FOR DYES & LADDERS** #
    for dye_dict in all_dyes:
      name = dye_dict['dye'].name
      lot_number = dye_dict['dye'].lot_number

      if dye_dict['dye'].is_expired:
        messages.error(request, f"Dye: {name} lot#: {lot_number} is expired.")
        return redirect(request.path_info)

      if dye_dict['dye'].amount - dye_dict['total'] < 0:
        name = dye_dict['dye'].name
        lot_number = dye_dict['dye'].lot_number
        messages.error(request, f"Dye: {name} lot#: {lot_number} has an insufficient amount for this process.  {round(dye_dict['total'], 2)}µl is required. Please update inventory or change selection.")
        return redirect(request.path_info)
      
    for ladder_dict in all_ladders:
      name = ladder_dict['ladder'].name
      lot_number = ladder_dict['ladder'].lot_number

      if ladder_dict['ladder'].is_expired:
        messages.error(request, f"Ladder: {name} lot#: {lot_number} is expired.")
        return redirect(request.path_info)
    
      if ladder_dict['ladder'].amount - ladder_dict['total'] < 0:
        messages.error(request, f"Ladder: {name} lot#: {lot_number} has an insufficient amount for this process.  {round(ladder_dict['total'], 2)}µl is required. Please update inventory or change selection.")
        return redirect(request.path_info)
    # **VALIDATION FOR DYES & LADDERS** #
      
    process.is_processed = True
    process.date_processed = timezone.now()

    process.pcr_dna_json = dna_pcr_json
    process.pcr_rna_json = rna_pcr_json
    process.pcr_gels_json = pcr_gels_json

    process.qpcr_dna_json = dna_qpcr_json
    process.qpcr_rna_json = rna_qpcr_json

    qpcr_plates_json = []
    for plate in qpcr_plates:
      qpcr_plates_json.append({'name': plate['name'], 'catalog_number': plate['catalog_number'], 'lot_number': plate['lot_number'], 'size': plate['size'], 'amount': plate['amount'], 'used': plate['used']})

    pcr_plates_json = []
    for plate in pcr_plates:
      pcr_plates_json.append({'name': plate['name'], 'catalog_number': plate['catalog_number'], 'lot_number': plate['lot_number'], 'size': plate['size'], 'amount': plate['amount'], 'used': plate['used']})

    gels_json = []
    for gel in gels:
      gels_json.append({'name': gel['name'], 'catalog_number': gel['catalog_number'], 'lot_number': gel['lot_number'], 'size': gel['size'], 'amount': gel['amount'], 'used': gel['used']})

    process.plates_for_qpcr = qpcr_plates_json
    process.plates_for_pcr = pcr_plates_json
    process.gels = gels_json

    reagent_usage_json = []
    for reagent in reagent_usage:
      reagent_data = {'name': reagent['reagent'].name, 'catalog_number': reagent['reagent'].catalog_number, 'lot_number': reagent['reagent'].lot_number, 'usage': reagent['usage']}
      reagent_usage_json.append(reagent_data)

    control_usage_json = []
    for control in control_usage:
      control_data = {'name': control['control'].name, 'lot_number': control['control'].lot_number, 'usage': control['usage']}
      control_usage_json.append(control_data)

    process.reagent_usage = reagent_usage_json
    process.control_usage = control_usage_json

    array = []
    for sample in process.samples.all():
      array.append(sample.batch)
    batches = list(set(array))

    process.batches.clear()
    for batch in batches:
      process.batches.add(batch)
    
    process.save()

    # **ALERT DATA** #
    inventory_alerts = {
      'date': process.date_processed,
      'qpcr_plates': [],
      'pcr_plates': [],
      'gels': [],
      'controls': [],
      'reagents': [],
      'dyes': [],
      'ladders': [],
    }

    # **FINAL UPDATE OF ALL PLATES AND GELS IN DB** #
    for plate in qpcr_plates:

      if plate['plate'].threshold > 0:
        diff = plate['plate'].amount - plate['used'] - plate['plate'].threshold 
        plate['plate'].threshold_diff = diff

        if diff <= 0:
          inventory_alerts['qpcr_plates'].append({
            'plate': plate['plate'].name, 
            'lot': plate['plate'].lot_number,
            'cat': plate['plate'].catalog_number,
            'amount': plate['plate'].amount,
            })

      plate['plate'].amount -= plate['used']
      plate['plate'].save()
      plate.pop('plate')

    for plate in pcr_plates:

      if plate['plate'].threshold > 0:
        plate['plate'].threshold_diff = plate['plate'].amount - plate['used'] - plate['plate'].threshold 

      plate['plate'].amount -= plate['used']
      plate['plate'].save()
      plate.pop('plate')

    for gel in gels:

      if plate['plate'].threshold > 0:
        plate['plate'].threshold_diff = plate['plate'].amount - plate['used'] - plate['plate'].threshold 

      gel['gel'].amount -= gel['used']
      gel['gel'].save()
      gel.pop('gel')
    # **FINAL UPDATE OF ALL PLATES AND GELS IN DB** #
      

    # **FINAL UPDATE OF ALL CONTROLS IN DB** #
    for control_dict in all_controls:
      control_dict['control'].amount -= Decimal(control_dict['total'])
      control_dict['control'].save()
    # **FINAL UPDATE OF ALL CONTROLS IN DB** #
      

    # **FINAL UPDATE OF ALL REAGENTS IN DB** #
    for reagent_dict in all_reagents:

      if reagent_dict['reagent'].threshold > 0:
        reagent_dict['reagent'].threshold_diff = Decimal(reagent_dict['reagent'].volume_in_microliters - reagent_dict['total'] - reagent_dict['reagent'].threshold_in_microliters)

      if process.is_plus_one_well == True:
        reagent_dict['reagent'].volume = Decimal(reagent_dict['reagent'].volume_in_microliters - reagent_dict['total'] - reagent_dict['volume_per_sample'])
      else:
        reagent_dict['reagent'].volume = Decimal(reagent_dict['reagent'].volume_in_microliters - reagent_dict['total'])

      reagent_dict['reagent'].unit_volume = Reagent.VolumeUnits.MICROLITER
      reagent_dict['reagent'].save()
    # **FINAL UPDATE OF ALL REAGENTS IN DB** #
      

    # **FINAL UPDATE OF ALL DYES & LADDERS IN DB** #
    for dye_dict in all_dyes:

      if dye_dict['dye'].threshold > 0:
        dye_dict['dye'].threshold_diff = Decimal(dye_dict['amount'] - dye_dict['total'] - dye_dict['dye'].threshold)

      dye_dict['dye'].amount -= dye_dict['total']
      dye_dict['dye'].save()

    for ladder_dict in all_ladders:

      if ladder_dict['ladder'].threshold > 0:
        ladder_dict['ladder'].threshold_diff = Decimal(ladder_dict['amount'] - ladder_dict['total'] - ladder_dict['ladder'].threshold)

      ladder_dict['ladder'].amount -= ladder_dict['total']
      ladder_dict['ladder'].save()
    # **FINAL UPDATE OF ALL DYES & LADDERS IN DB** #

    # **ALERT DATA** #
      
    return redirect('processes')

  context = {
    'dna_qpcr_json': dna_qpcr_json, 'rna_qpcr_json': rna_qpcr_json, 
    'dna_pcr_json': dna_pcr_json, 'rna_pcr_json': rna_pcr_json, 
    'qpcr_plates': qpcr_plates, 'pcr_plates': pcr_plates, 'gels': gels,
    'pcr_gels_json': pcr_gels_json, 'process': process, 
    'reagent_usage': reagent_usage, 'control_usage': control_usage
    }
  return render(request, 'pcr/process_paperwork.html', context)


@login_required(login_url='login')
def processes(request):
  processes = Process.objects.filter(user=request.user, is_processed=True).order_by('-date_processed')

  form = SearchProcessForm(user=request.user)
  if request.method == "GET":
    form = SearchProcessForm(request.GET, user=request.user)
    if form.is_valid():
      name = form.cleaned_data['name']
      panel = form.cleaned_data['panel']
      lab_id = form.cleaned_data['lab_id']
      start_date = form.cleaned_data['start_date']
      end_date = form.cleaned_data['end_date']

      filters = {}
      if name:
        filters['name__icontains'] = name
      if panel:
        filters['batches__code'] = panel
      if lab_id:
        filters['batches__lab_id'] = lab_id

      if start_date and not end_date:
        day = start_date + datetime.timedelta(days=1)
        filters['date_processed__range'] = [start_date, day]

      if end_date and not start_date:
        day = end_date + datetime.timedelta(days=1)
        filters['date_processed__range'] = [end_date, day]
      
      if start_date and end_date:
        end_date += datetime.timedelta(days=1)
        filters['date_processed__range'] = [start_date, end_date]

      processes = Process.objects.filter(user=request.user, is_processed=True, **filters).order_by('-date_processed')
    else:
      print(form.errors)

  paginator = Paginator(processes, 25)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)
  
  context = {'page_obj': page_obj, 'form': form}
  return render(request, 'pcr/processes.html', context)


@login_required(login_url='login')
def pcr_paperwork(request, pk):
  try:
    process = Process.objects.get(user=request.user, is_processed=True, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no process to review.")
    return redirect('processes')
  
  context = {
    'dna_qpcr_json': process.qpcr_dna_json, 'rna_qpcr_json': process.qpcr_rna_json, 
    'dna_pcr_json': process.pcr_dna_json, 'rna_pcr_json': process.pcr_rna_json, 
    'process': process, 'pcr_gels_json': process.pcr_gels_json,
    'reagent_usage': process.reagent_usage, 'control_usage': process.control_usage
  }
  return render(request, 'pcr/pcr_paperwork.html', context)