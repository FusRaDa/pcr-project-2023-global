from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import math

from ..models.batch import Batch, Sample
from ..models.assay import Assay
from ..models.inventory import Plate
from ..models.inventory import Reagent
from ..models.pcr import Process


def create_samples(number_of_samples, lab_id, user, negative_control):
  batch = Batch.objects.get(user=user, lab_id=lab_id)
  assays = batch.code.assays.all()
  
  # create samples for the batch
  for i in range(number_of_samples):

    i += 1
    sample = Sample.objects.create(
      user = user,
      lab_id_num = lab_id + "-" + str(i),
      batch = batch,
    )

    sample.assays.add(*assays)

  if negative_control == True:
    control = Sample.objects.create(
      user = user,
      lab_id_num = lab_id + "-" + str(number_of_samples + 1) + " (NC)",
      sample_id = "NegCtrl-Water",
      batch = batch,
    )

    control.assays.add(*assays)

def samples_by_assay(samples):
  all_assays = []
  for sample in samples:
    for assay in sample.assays.all():
      all_assays.append(assay)
  assays = list(set(all_assays))
  sorted_assays = sorted(assays, key=lambda x: x.name, reverse=False)

  assay_samples = []
  for assay in sorted_assays:
    x = {assay:[]}
    for sample in samples:
      if sample.assays.contains(assay):
        x[assay].append(sample)
    assay_samples.append(x)
  return assay_samples


def samples_by_assay_multiplicates(samples):
  all_assays = []
  for sample in samples:
    for assay in sample.assays.all():
      all_assays.append(assay)
  assays = list(set(all_assays))
  sorted_assays = sorted(assays, key=lambda x: x.name, reverse=False)

  assay_samples = []
  for assay in sorted_assays:
    
    multiplicates = assay.multiplicates
    while multiplicates > 0:
      x = {assay:[]}
      for sample in samples:
        if sample.assays.contains(assay):
          x[assay].append(sample)
      assay_samples.append(x)
      multiplicates -= 1

  return assay_samples


def dna_qpcr_samples(assay_samples): 
  colors = ['table-primary', 'table-secondary', 'table-success', 'table-danger', 'table-warning', 'table-info', 'table-light', 'table-dark']

  # collect all samples that are for DNA in PCR by assay
  all_samples = []
  color = 0
  for index in assay_samples:
    for assay, samples in index.items():
      if assay.method == Assay.Methods.qPCR and assay.type == Assay.Types.DNA:
    
        data = []
        for sample in samples:
          sample_data = {None:{
            'color': colors[color],
            'lab_id': sample.lab_id_num,
            'sample_id': sample.sample_id,
            'assay': assay.name
          }}
          data.append(sample_data)
     
        color += 1
        if color > 7:
          color = 0
        assay_data = {assay: data}
        all_samples.append(assay_data)
  return all_samples


def rna_qpcr_samples(assay_samples):
  colors = ['table-primary', 'table-secondary', 'table-success', 'table-danger', 'table-warning', 'table-info', 'table-light', 'table-dark']

  all_samples = []
  color = 0
  for index in assay_samples:
    for assay, samples in index.items():
      if assay.method == Assay.Methods.qPCR and assay.type == Assay.Types.RNA:
    
        data = []
        for sample in samples:
          sample_data = {None:{
            'color': colors[color],
            'lab_id': sample.lab_id_num,
            'sample_id': sample.sample_id,
            'assay': assay.name
          }}
          data.append(sample_data)
     
        color += 1
        if color > 7:
          color = 0
        assay_data = {assay: data}
        all_samples.append(assay_data)
  return all_samples


def dna_pcr_samples(assay_samples):
  colors = ['table-primary', 'table-secondary', 'table-success', 'table-danger', 'table-warning', 'table-info', 'table-light', 'table-dark']

  all_samples = []
  color = 0
  for index in assay_samples:
    for assay, samples in index.items():
      if assay.method == Assay.Methods.PCR and assay.type == Assay.Types.DNA:
    
        data = []
        for sample in samples:
          sample_data = {None:{
            'color': colors[color],
            'lab_id': sample.lab_id_num,
            'sample_id': sample.sample_id,
            'assay': assay.name
          }}
          data.append(sample_data)
     
        color += 1
        if color > 7:
          color = 0
        assay_data = {assay: data}
        all_samples.append(assay_data)
  return all_samples


def rna_pcr_samples(assay_samples):
  colors = ['table-primary', 'table-secondary', 'table-success', 'table-danger', 'table-warning', 'table-info', 'table-light', 'table-dark']

  all_samples = []
  color = 0
  for index in assay_samples:
    for assay, samples in index.items():
      if assay.method == Assay.Methods.PCR and assay.type == Assay.Types.RNA:
    
        data = []
        for sample in samples:
          sample_data = {None:{
            'color': colors[color],
            'lab_id': sample.lab_id_num,
            'sample_id': sample.sample_id,
            'assay': assay.name
          }}
          data.append(sample_data)
     
        color += 1
        if color > 7:
          color = 0
        assay_data = {assay: data}
        all_samples.append(assay_data)
  return all_samples


def all_pcr_samples(assay_samples):
  colors = ['table-primary', 'table-secondary', 'table-success', 'table-danger', 'table-warning', 'table-info', 'table-light', 'table-dark']

  all_samples = []
  color = 0
  for index in assay_samples:
    for assay, samples in index.items():
      if assay.method == Assay.Methods.PCR and assay.type == Assay.Types.DNA:
    
        data = []
        for sample in samples:
          sample_data = {None:{
            'color': colors[color],
            'lab_id': sample.lab_id_num,
            'sample_id': sample.sample_id,
            'assay': assay.name
          }}
          data.append(sample_data)
     
        color += 1
        if color > 7:
          color = 0
        assay_data = {assay: data}
        all_samples.append(assay_data)

  for index in assay_samples:
    for assay, samples in index.items():
      if assay.method == Assay.Methods.PCR and assay.type == Assay.Types.RNA:
    
        data = []
        for sample in samples:
          sample_data = {None:{
            'color': colors[color],
            'lab_id': sample.lab_id_num,
            'sample_id': sample.sample_id,
            'assay': assay.name
          }}
          data.append(sample_data)
     
        color += 1
        if color > 7:
          color = 0
        assay_data = {assay: data}
        all_samples.append(assay_data)

  return all_samples


def choose_plate(all_samples, plates):
  total_wells_used = 0
  for assay_group in all_samples:
    for assay, samples in assay_group.items():
      if len(samples) > 0:
        total_wells_used += (len(samples) + assay.controls.count())

  chosen_plate = None     
  for plate in plates:
    if plate['plate'].size >= total_wells_used and plate['amount'] > 0:
      plate['amount'] -= 1
      plate['used'] += 1
      chosen_plate = plate['plate']
      break

  if chosen_plate == None:
    rev_list = sorted(plates, key=lambda x: x['size'], reverse=True)
    for plate in rev_list:
      if plate['amount'] > 0:
        plate['amount'] -= 1
        plate['used'] += 1
        chosen_plate = plate['plate']
        break
  
  if chosen_plate == None:
    rev_list[0]['amount'] -= 1
    rev_list[0]['used'] += 1
    chosen_plate = rev_list[0]['plate']

  return chosen_plate, plates
 

def choose_gel(all_samples, gels):
  total_wells_used = 0
  for assay_group in all_samples:
    for assay, samples in assay_group.items():
      if len(samples) > 0:
        total_wells_used += (len(samples) + assay.controls.count())

  chosen_gel = None
  for gel in gels:
    if gel['gel'].size >= total_wells_used and gel['amount'] > 0:
      gel['amount'] -= 1
      gel['used'] += 1
      chosen_gel = gel['gel']
      break
  
  if chosen_gel == None:
    rev_list = sorted(gels, key=lambda x: x['size'], reverse=True)
    for plate in rev_list:
      if plate['amount'] > 0:
        plate['amount'] -= 1
        plate['used'] += 1
        chosen_gel = plate['gel']
        break
  
  if chosen_gel == None:
    rev_list[0]['amount'] -= 1
    rev_list[0]['used'] += 1
    chosen_gel = rev_list[0]['gel']
  
  return chosen_gel, gels


def organized_plate(all_samples, plate, samples_data, primers_data, assays_data, minimum_samples_in_plate, remaining_wells, position):
  for data in all_samples:

    if remaining_wells == 0:
      break
    
    for assay, samples in data.items():

      if len(samples) != 0:

        loaded_samples = [] # collect keys to delete later after samples have been added to the json file
        control_color = samples[0][None]['color']
        
        sample_wells = len(samples)
        control_wells = assay.controls.count()
        total_wells = sample_wells + control_wells

        if total_wells < remaining_wells: # LOGIC HELP

          num_samples = 0
          for sample in samples:
            num_samples += 1
            position += 1
            sample[f"well{position}"] = sample[None]
            del sample[None]
            loaded_samples.append(sample)
            samples_data['samples'].update(sample)

          assay_dict = {
            'name': assay.name,
            'sample_num': num_samples + control_wells,
            'sample_volume': round(float(assay.sample_volume), 2),
            'reaction_volume': round(float(assay.reaction_volume), 2),
            'mm_volume': round(float(assay.mm_volume), 2),
            'fluorescence': [],
            'controls': assay.controls.all(),
            'reagents': [],
          }

          for fluor in assay.fluorescence.all():
            assay_dict['fluorescence'].append(fluor.name)
          
          for reagent in assay.reagentassay_set.all().order_by('order'):
            stock_concentration = None
            if reagent.reagent.stock_concentration:
              stock_concentration = round(float(reagent.reagent.stock_concentration), 2)

            final_stock_concentration = None
            if reagent.final_concentration:
              final_stock_concentration = round(float(reagent.final_concentration), 2)

            dilution_factor = None
            if reagent.dilution_factor:
              dilution_factor = round(float(reagent.dilution_factor), 2)

            assay_dict['reagents'].append({
              'reagent': reagent.reagent,
              'name': reagent.reagent.name,
              'volume_per_sample': round(float(reagent.volume_per_sample), 2),
              'stock_concentration': stock_concentration,
              'unit_concentration': reagent.reagent.unit_concentration,
              'final_stock_concentration': final_stock_concentration,
              'final_unit_concentration': reagent.final_concentration_unit,
              'dilution_factor': dilution_factor,
            })

            if reagent.reagent.pcr_reagent == Reagent.PCRReagent.PRIMER:
              primer_dict = {
                'pk': reagent.reagent.pk, 
                'name': reagent.reagent.name, 
                'forward_sequence': reagent.reagent.forward_sequence, 
                'reverse_sequence': reagent.reagent.reverse_sequence, 
                'assay': assay.name
              }
              primers_data['primers'].append(primer_dict)

          assays_data['assays'].append(assay_dict)

          # add validation if plate size is insufficient to even hold only one assay w/ controls
          if plate.size == Plate.Sizes.EIGHT:
            wells_in_row = 1

          if plate.size == Plate.Sizes.TWENTY_FOUR:
            wells_in_row = 3

          if plate.size == Plate.Sizes.FOURTY_EIGHT:
            wells_in_row = 6 

          if plate.size == Plate.Sizes.NINETY_SIX:
            wells_in_row = 12

          if plate.size == Plate.Sizes.THREE_HUNDRED_EIGHTY_FOUR:
            wells_in_row = 24

          # find what row last sample is located in and how many available wells are in that row
          row = math.floor(position / wells_in_row) + 1
          if position % wells_in_row == 0: # if position is the last on the row make sure it is assigned to the proper row
            row -= 1
          rem_wells_in_row = (row * wells_in_row) - position

          # if there is enough room in the same row add controls
          if control_wells <= rem_wells_in_row:
            block = (row * wells_in_row)
            start = block - control_wells
            cwells = []
            for n in range(start + 1, block + 1):
              cwells.append(n)
          
            zip_data = zip(assay.controlassay_set.all().order_by('order'), cwells)
      
            for control, well in zip_data:
              control_data = {f"well{well}": {
                'color': control_color,
                'lab_id': control.control.name,
                'sample_id': control.control.lot_number,
                'assay': assay.name
              }}
              samples_data['samples'].update(control_data)

            remaining_wells = (plate.size - block)
            position = block
          
          else:
            # move to next row only if plate size is not 8 - since there is no "row"
            if plate.size != Plate.Sizes.EIGHT:
              row += 1
              block = (row * wells_in_row)
              start = block - control_wells
              cwells = []
              for n in range(start + 1, block + 1):
                cwells.append(n)

              zip_data = zip(assay.controlassay_set.all().order_by('order'), cwells)
        
              for control, well in zip_data:
                control_data = {f"well{well}": {
                  'color': control_color,
                  'lab_id': control.control.name,
                  'sample_id': control.control.lot_number,
                  'assay': assay.name
                }}
                samples_data['samples'].update(control_data)

              remaining_wells = (plate.size - block)
              position = block

            # FOR 8-WELL PLATE ONLY TO ADD CONTROLS #
            else:
              for control in assay.controlassay_set.all().order_by('order'):
                position += 1
                control_data = {f"well{position}": {
                  'color': control_color,
                  'lab_id': control.control.name,
                  'sample_id': control.control.lot_number,
                  'assay': assay.name
                }}
                samples_data['samples'].update(control_data)
              remaining_wells -= position
            # FOR 8-WELL PLATE ONLY TO ADD CONTROLS #
              
        # comment - if assay samples wont fit in remaining wells... (total wells > remaining_wells)
        else:
          # create validation for minimum_samples_in_plate where it cannot be negative or greater than smallest plate size. 
          if minimum_samples_in_plate + control_wells <= remaining_wells:
            
            num_samples = 0
            for sample in samples[:remaining_wells - control_wells]:
              num_samples += 1
              position += 1
              sample[f"well{position}"] = sample[None]
              del sample[None]
              loaded_samples.append(sample)
              samples_data['samples'].update(sample)
            
            assay_dict = {
              'name': assay.name,
              'sample_num': num_samples + control_wells,
              'sample_volume': round(float(assay.sample_volume), 2),
              'reaction_volume': round(float(assay.reaction_volume), 2),
              'mm_volume': round(float(assay.mm_volume), 2),
              'fluorescence': [],
              'controls': assay.controls.all(),
              'reagents': [],
            }

            for fluor in assay.fluorescence.all():
              assay_dict['fluorescence'].append(fluor.name)
            
            for reagent in assay.reagentassay_set.all().order_by('order'):
              stock_concentration = None
              if reagent.reagent.stock_concentration:
                stock_concentration = round(float(reagent.reagent.stock_concentration), 2)

              final_stock_concentration = None
              if reagent.final_concentration:
                final_stock_concentration = round(float(reagent.final_concentration), 2)

              dilution_factor = None
              if reagent.dilution_factor:
                dilution_factor = round(float(reagent.dilution_factor), 2)

              assay_dict['reagents'].append({
                'reagent': reagent.reagent,
                'name': reagent.reagent.name,
                'volume_per_sample': round(float(reagent.volume_per_sample), 2),
                'stock_concentration': stock_concentration,
                'unit_concentration': reagent.reagent.unit_concentration,
                'final_stock_concentration': final_stock_concentration,
                'final_unit_concentration': reagent.final_concentration_unit,
                'dilution_factor': dilution_factor,
              })

              if reagent.reagent.pcr_reagent == Reagent.PCRReagent.PRIMER:
                primer_dict = {
                'pk': reagent.reagent.pk, 
                'name': reagent.reagent.name, 
                'forward_sequence': reagent.reagent.forward_sequence, 
                'reverse_sequence': reagent.reagent.reverse_sequence, 
                'assay': assay.name
                }
                primers_data['primers'].append(primer_dict)

            assays_data['assays'].append(assay_dict)

            for control in assay.controlassay_set.all().order_by('order'):
              position += 1
              control_data = {f"well{position}": {
                'color': control_color,
                'lab_id': control.control.name,
                'sample_id': control.control.lot_number,
                'assay': assay.name
              }}
              samples_data['samples'].update(control_data)
            remaining_wells = 0
          else:
            remaining_wells = 0
         
        # remove samples from list that have already been loaded into plate
        for sample in loaded_samples:
          samples.remove(sample)


def compressed_plate(all_samples, plate, samples_data, primers_data, assays_data, minimum_samples_in_plate, remaining_wells, position):
  for data in all_samples:

    if remaining_wells == 0:
      break
    
    for assay, samples in data.items():

      if len(samples) != 0:

        loaded_samples = [] # collect keys to delete later after samples have been added to the json file
        control_color = samples[0][None]['color']
        
        sample_wells = len(samples)
        control_wells = assay.controls.count()
        total_wells = sample_wells + control_wells

        if total_wells < remaining_wells: # LOGIC HELP

          num_samples = 0
          for sample in samples:
            num_samples += 1
            position += 1
            sample[f"well{position}"] = sample[None]
            del sample[None]
            loaded_samples.append(sample)
            samples_data['samples'].update(sample)

          for control in assay.controlassay_set.all().order_by('order'):
            position += 1
            control_data = {f"well{position}": {
              'color': control_color,
              'lab_id': control.control.name,
              'sample_id': control.control.lot_number,
              'assay': assay.name
            }}
            samples_data['samples'].update(control_data)

          remaining_wells = plate.size - position
          
          assay_dict = {
            'name': assay.name,
            'sample_num': num_samples + control_wells,
            'sample_volume': round(float(assay.sample_volume), 2),
            'reaction_volume': round(float(assay.reaction_volume), 2),
            'mm_volume': round(float(assay.mm_volume), 2),
            'fluorescence': [],
            'controls': assay.controls.all(),
            'reagents': [],
          }

          for fluor in assay.fluorescence.all():
            assay_dict['fluorescence'].append(fluor.name)
          
          for reagent in assay.reagentassay_set.all().order_by('order'):
            stock_concentration = None
            if reagent.reagent.stock_concentration:
              stock_concentration = round(float(reagent.reagent.stock_concentration), 2)

            final_stock_concentration = None
            if reagent.final_concentration:
              final_stock_concentration = round(float(reagent.final_concentration), 2)

            dilution_factor = None
            if reagent.dilution_factor:
              dilution_factor = round(float(reagent.dilution_factor), 2)

            assay_dict['reagents'].append({
              'reagent': reagent.reagent,
              'name': reagent.reagent.name,
              'volume_per_sample': round(float(reagent.volume_per_sample), 2),
              'stock_concentration': stock_concentration,
              'unit_concentration': reagent.reagent.unit_concentration,
              'final_stock_concentration': final_stock_concentration,
              'final_unit_concentration': reagent.final_concentration_unit,
              'dilution_factor': dilution_factor,
            })

            if reagent.reagent.pcr_reagent == Reagent.PCRReagent.PRIMER:
              primer_dict = {
                'pk': reagent.reagent.pk, 
                'name': reagent.reagent.name, 
                'forward_sequence': reagent.reagent.forward_sequence, 
                'reverse_sequence': reagent.reagent.reverse_sequence, 
                'assay': assay.name
              }
              primers_data['primers'].append(primer_dict)

          assays_data['assays'].append(assay_dict)

        else:
          # create validation for minimum_samples_in_plate where it cannot be negative or greater than smallest plate size. 
          if minimum_samples_in_plate + control_wells <= remaining_wells:

            num_samples = 0
            for sample in samples[:remaining_wells - control_wells]:
              num_samples += 1
              position += 1
              sample[f"well{position}"] = sample[None]
              del sample[None]
              loaded_samples.append(sample)
              samples_data['samples'].update(sample)

            for control in assay.controlassay_set.all().order_by('order'):
              position += 1
              control_data = {f"well{position}": {
                'color': control_color,
                'lab_id': control.control.name,
                'sample_id': control.control.lot_number,
                'assay': assay.name
              }}
              samples_data['samples'].update(control_data)
            
            assay_dict = {
              'name': assay.name,
              'sample_num': num_samples + control_wells,
              'sample_volume': round(float(assay.sample_volume), 2),
              'reaction_volume': round(float(assay.reaction_volume), 2),
              'mm_volume': round(float(assay.mm_volume), 2),
              'fluorescence': [],
              'controls': assay.controls.all(),
              'reagents': [],
            }

            for fluor in assay.fluorescence.all():
              assay_dict['fluorescence'].append(fluor.name)
            
            for reagent in assay.reagentassay_set.all().order_by('order'):
              stock_concentration = None
              if reagent.reagent.stock_concentration:
                stock_concentration = round(float(reagent.reagent.stock_concentration), 2)

              final_stock_concentration = None
              if reagent.final_concentration:
                final_stock_concentration = round(float(reagent.final_concentration), 2)

              dilution_factor = None
              if reagent.dilution_factor:
                dilution_factor = round(float(reagent.dilution_factor), 2)

              assay_dict['reagents'].append({
                'reagent': reagent.reagent,
                'name': reagent.reagent.name,
                'volume_per_sample': round(float(reagent.volume_per_sample), 2),
                'stock_concentration': stock_concentration,
                'unit_concentration': reagent.reagent.unit_concentration,
                'final_stock_concentration': final_stock_concentration,
                'final_unit_concentration': reagent.final_concentration_unit,
                'dilution_factor': dilution_factor,
              })

              if reagent.reagent.pcr_reagent == Reagent.PCRReagent.PRIMER:
                primer_dict = {
                'pk': reagent.reagent.pk, 
                'name': reagent.reagent.name, 
                'forward_sequence': reagent.reagent.forward_sequence, 
                'reverse_sequence': reagent.reagent.reverse_sequence, 
                'assay': assay.name
                }
                primers_data['primers'].append(primer_dict)

            assays_data['assays'].append(assay_dict)

            remaining_wells = 0
          else:
            remaining_wells = 0
         
        # remove samples from list that have already been loaded into plate
        for sample in loaded_samples:
          samples.remove(sample)


def load_plate(all_samples, plates, protocol, minimum_samples_in_plate, loading_method):
  plate, list = choose_plate(all_samples, plates)

  plate_data = {'size': plate.size}
  protocol_data = {'protocol': {
    'name': protocol.name,
    'denature_temp': round(float(protocol.denature_temp), 2),
    'denature_duration': protocol.denature_duration,
    'anneal_temp': round(float(protocol.anneal_temp), 2),
    'anneal_duration': protocol.anneal_duration,
    'extension_temp': round(float(protocol.extension_temp), 2),
    'extension_duration': protocol.extension_duration,
    'number_of_cycles': protocol.number_of_cycles
  }}
  assays_data = {'assays': []}
  samples_data = {'samples': {}}
  primers_data = {'primers': []}

  remaining_wells = plate.size
  position = 0
  
  if loading_method == Process.LoadingMethod.ORGANIZED:
    organized_plate(
      all_samples=all_samples,
      plate=plate,
      samples_data=samples_data,
      primers_data=primers_data,
      assays_data=assays_data,
      minimum_samples_in_plate=minimum_samples_in_plate,
      remaining_wells=remaining_wells,
      position=position,
    )

  if loading_method == Process.LoadingMethod.COMPRESSED:
    compressed_plate(
      all_samples=all_samples,
      plate=plate,
      samples_data=samples_data,
      primers_data=primers_data,
      assays_data=assays_data,
      minimum_samples_in_plate=minimum_samples_in_plate,
      remaining_wells=remaining_wells,
      position=position,
    )

  sorted_primers_data = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in primers_data['primers'])]
  primers_data['primers'].clear()
  primers_data['primers'] = sorted_primers_data

  # create plate dictionary that contains plate, tcprotocol, assays, and samples
  plate_dict = protocol_data | plate_data | assays_data | samples_data | primers_data
  return plate_dict, all_samples


def load_gel(all_samples, gels, minimum_samples_in_gel):
  gel, list = choose_gel(all_samples, gels)

  gel_data = {'size': gel.size}
  samples_data = {'samples': {}}
  dyes_data = {'dyes': []}
  ladders_data = {'ladders': []}

  remaining_wells = gel.size
  position = 0

  for data in all_samples:

    if remaining_wells == 0:
      break

    for assay, samples in data.items():
      if len(samples) != 0:

        loaded_samples = [] # collect keys to delete later after samples have been added to the json file
        control_color = samples[0][None]['color']

        sample_wells = len(samples)
        control_wells = assay.controls.count()
        total_wells = sample_wells + control_wells + 1

        if total_wells <= remaining_wells:

          num_samples = 0
          for sample in samples:
            num_samples += 1
            position += 1
            sample[f"well{position}"] = sample[None]
            del sample[None]
            loaded_samples.append(sample)
            samples_data['samples'].update(sample)

          dye_dict = {
            'dye': assay.dye,
            'name': f"{assay.dye.name} - {assay.name}",
            'sample_num': num_samples + control_wells,
            'volume_per_well': round(float(assay.dye_volume_per_well), 2),
            'dye_in_ladder': assay.dye_in_ladder,
          }
          dyes_data['dyes'].append(dye_dict)
          
          for control in assay.controlassay_set.all().order_by('order'):
            position += 1
            control_data = {f"well{position}": {
              'color': control_color,
              'lab_id': control.control.name,
              'sample_id':control.control.lot_number,
              'assay': assay.name
            }}
            samples_data['samples'].update(control_data)

          ladder_dict = {
            'ladder': assay.ladder,
            'name': f"{assay.ladder.name} - {assay.name}",
            'volume_per_gel': round(float(assay.ladder_volume_per_gel), 2),
          }
          ladders_data['ladders'].append(ladder_dict)
          
          position += 1
          ladder = {f"well{position}": {
              'color': control_color,
              'lab_id': assay.ladder.name,
              'sample_id': f"Cat#{assay.ladder.catalog_number} Lot#{assay.ladder.lot_number}",
              'assay': assay.name
            }}
          samples_data['samples'].update(ladder)
          remaining_wells -= position

        else: 
          if minimum_samples_in_gel + control_wells + 1 <= remaining_wells:
            num_samples = 0
            for sample in samples[:remaining_wells - control_wells - 1]:
              num_samples += 1
              position += 1
              sample[f"well{position}"] = sample[None]
              del sample[None]
              loaded_samples.append(sample)
              samples_data['samples'].update(sample)

            dye_dict = {
              'dye': assay.dye,
              'name': f"{assay.dye.name} - {assay.name}",
              'sample_num': num_samples + control_wells,
              'volume_per_well': round(float(assay.dye_volume_per_well), 2),
              'dye_in_ladder': assay.dye_in_ladder,
            }
            dyes_data['dyes'].append(dye_dict)
            
            for control in assay.controlassay_set.all().order_by('order'):
              position += 1
              control_data = {f"well{position}": {
                'color': control_color,
                'lab_id': control.control.name,
                'sample_id':control.control.lot_number,
                'assay': assay.name
              }}
              samples_data['samples'].update(control_data)

            ladder_dict = {
              'ladder': assay.ladder,
              'name': f"{assay.ladder.name} - {assay.name}",
              'volume_per_gel': round(float(assay.ladder_volume_per_gel), 2),
            }
            ladders_data['ladders'].append(ladder_dict)
            
            position += 1
            ladder = {f"well{position}": {
                'color': control_color,
                'lab_id': assay.ladder.name,
                'sample_id': f"Cat#{assay.ladder.catalog_number} Lot#{assay.ladder.lot_number}",
                'assay': assay.name
              }}
            samples_data['samples'].update(ladder)
            remaining_wells = 0
          else:
            remaining_wells = 0
        
        for sample in loaded_samples:
          samples.remove(sample)
     
  gel_dict = gel_data | samples_data | dyes_data | ladders_data
  return gel_dict, all_samples


def process_plates(all_samples, plates, protocol, minimum_samples_in_plate, loading_method):
  qpcr_data = []

  is_empty = False
  while not is_empty:
 
    plate_dict, all_samples = load_plate(all_samples, plates, protocol, minimum_samples_in_plate, loading_method)
    qpcr_data.append(plate_dict)

    # check if all samples for each assay is empty if not continue the process of making plates
    for data in all_samples:
      for assay, samples in data.items():
        if len(samples) == 0:
          is_empty = True
        else:
          is_empty = False
  
  return qpcr_data


def process_gels(all_samples, gels, minimum_samples_in_gel):
  pcr_data = []

  is_empty = False
  while not is_empty:

    gel_dict, all_samples = load_gel(all_samples, gels, minimum_samples_in_gel)
    pcr_data.append(gel_dict)


    for data in all_samples:
      for assay, samples in data.items():
        if len(samples) == 0:
          is_empty = True
        else:
          is_empty = False
    
  return pcr_data


def detect_inventory_usage(ladders, dyes, plates, gels, tubes, reagents, controls):
  ladders_warn = False
  dyes_warn = False
  plates_warn = False
  gels_warn = False
  tubes_warn = False
  reagents_warn = False
  controls_warn = False

  for ladder in ladders:
    if ladder.is_expired or ladder.month_exp or (ladder.threshold_diff is not None and ladder.threshold_diff <= 0):
      ladders_warn = True
      break

  for dye in dyes:
    if dye.is_expired or dye.month_exp or (dye.threshold_diff is not None and dye.threshold_diff <= 0):
      dyes_warn = True
      break

  for plate in plates:
    if plate.is_expired or plate.month_exp or (plate.threshold_diff is not None and plate.threshold_diff <= 0):
      plates_warn = True
      break

  for gel in gels:
    if gel.is_expired or gel.month_exp or (gel.threshold_diff is not None and gel.threshold_diff <= 0):
      gels_warn = True
      break

  for tube in tubes:
    if tube.is_expired or tube.month_exp or (tube.threshold_diff is not None and tube.threshold_diff <= 0):
      tubes_warn = True
      break

  for reagent in reagents:
    if reagent.is_expired or reagent.month_exp or (reagent.threshold_diff is not None and reagent.threshold_diff <= 0):
      reagents_warn = True
      break

  for control in controls:
    if control.is_expired or control.month_exp or control.amount <= 100:
      controls_warn = True
      break

  message = None
  if ladders_warn or dyes_warn or plates_warn or gels_warn or tubes_warn or reagents_warn or controls_warn:
    message = "Inventory for "

    if ladders_warn:
      message += "ladders, "

    if dyes_warn:
      message += "dyes, "

    if plates_warn:
      message += "plates, "

    if gels_warn:
      message += "gels, "

    if tubes_warn:
      message += "tubes, "

    if reagents_warn:
      message += "reagents, "

    if controls_warn:
      message += "controls, "

    message += "require your attention!"
  
  return message


def detect_mergeable_items(ladders, dyes, plates, gels, tubes, reagents, controls):
  ladders_warn = False
  dyes_warn = False
  plates_warn = False
  gels_warn = False
  tubes_warn = False
  reagents_warn = False
  controls_warn = False

  for index, val in enumerate(ladders):
    if index != ladders.count() - 1:
      if val.catalog_number == ladders[index + 1].catalog_number and val.name.lower() == ladders[index + 1].name.lower():
        ladders_warn = True
        break

  for index, val in enumerate(dyes):
    if index != dyes.count() - 1:
      if val.catalog_number == dyes[index + 1].catalog_number and val.name.lower() == dyes[index + 1].name.lower():
        dyes_warn = True
        break

  for index, val in enumerate(plates):
    if index != plates.count() - 1:
      if val.catalog_number == plates[index + 1].catalog_number and val.name.lower() == plates[index + 1].name.lower():
        plates_warn = True
        break
        
  for index, val in enumerate(gels):
    if index != gels.count() - 1:
      if val.catalog_number == gels[index + 1].catalog_number and val.name.lower() == gels[index + 1].name.lower():
        gels_warn = True
        break

  for index, val in enumerate(tubes):
    if index != tubes.count() - 1:
      if val.catalog_number == tubes[index + 1].catalog_number and val.name.lower() == tubes[index + 1].name.lower():
        tubes_warn = True
        break

  for index, val in enumerate(reagents):
    if index != reagents.count() - 1:
      if val.catalog_number == reagents[index + 1].catalog_number and val.name.lower() == reagents[index + 1].name.lower():
        reagents_warn = True
        break

  for index, val in enumerate(controls):
    if index != controls.count() - 1:
      if val.catalog_number == controls[index + 1].catalog_number and val.name.lower() == controls[index + 1].name.lower():
        controls_warn = True
        break

  message = None
  if ladders_warn or dyes_warn or plates_warn or gels_warn or tubes_warn or reagents_warn or controls_warn:
    message = "There are "

    if ladders_warn:
      message += "ladders, "

    if dyes_warn:
      message += "dyes, "

    if plates_warn:
      message += "plates, "

    if gels_warn:
      message += "gels, "

    if tubes_warn:
      message += "tubes, "

    if reagents_warn:
      message += "reagents, "

    if controls_warn:
      message += "controls, "

    message += "that you may merge."
  
  return message


def find_mergeable_items(ladders, dyes, plates, gels, tubes, reagents, controls):
  mergeable_dict = {
    'ladders': None,
    'dyes': None,
    'plates': None,
    'gels': None,
    'tubes': None,
    'reagents': None,
    'controls': None,
  }

  temp_ladders = []
  for index, val in enumerate(ladders):
    if index != ladders.count() - 1 and val.catalog_number != None:
      if val.catalog_number == ladders[index + 1].catalog_number and val.name.lower() == ladders[index + 1].name.lower():
        temp_ladders.append({'name': val.name, 'cat': val.catalog_number})
  dedupe_ladders = {str(item): item for item in temp_ladders} 
  mergeable_dict['ladders'] = dedupe_ladders.values()

  temp_dyes = []
  for index, val in enumerate(dyes):
    if index != dyes.count() - 1 and val.catalog_number != None:
      if val.catalog_number == dyes[index + 1].catalog_number and val.name.lower() == dyes[index + 1].name.lower():
        temp_dyes.append({'name': val.name, 'cat': val.catalog_number})
  dedupe_dyes = {str(item): item for item in temp_dyes} 
  mergeable_dict['dyes'] = dedupe_dyes.values()

  temp_plates = []
  for index, val in enumerate(plates):
    if index != plates.count() - 1 and val.catalog_number != None:
      if val.catalog_number == plates[index + 1].catalog_number and val.name.lower() == plates[index + 1].name.lower():
        temp_plates.append({'name': val.name, 'cat': val.catalog_number})
  dedupe_plates = {str(item): item for item in temp_plates}      
  mergeable_dict['plates'] = dedupe_plates.values()
  
  temp_gels = []
  for index, val in enumerate(gels):
    if index != gels.count() - 1 and val.catalog_number != None:
      if val.catalog_number == gels[index + 1].catalog_number and val.name.lower() == gels[index + 1].name.lower():
        temp_gels.append({'name': val.name, 'cat': val.catalog_number})
  dedupe_gels = {str(item): item for item in temp_gels} 
  mergeable_dict['gels'] = dedupe_gels.values()

  temp_tubes = []
  for index, val in enumerate(tubes):
    if index != tubes.count() - 1 and val.catalog_number != None:
      if val.catalog_number == tubes[index + 1].catalog_number and val.name.lower() == tubes[index + 1].name.lower():
        temp_tubes.append({'name': val.name, 'cat': val.catalog_number})
  dedupe_tubes = {str(item): item for item in temp_tubes} 
  mergeable_dict['tubes'] = dedupe_tubes.values()

  temp_reagents = []
  for index, val in enumerate(reagents):
    if index != reagents.count() - 1 and val.catalog_number != None:
      if val.catalog_number == reagents[index + 1].catalog_number and val.name.lower() == reagents[index + 1].name.lower():
        temp_reagents.append({'name': val.name, 'cat': val.catalog_number})
  dedupe_reagents = {str(item): item for item in temp_reagents} 
  mergeable_dict['reagents'] = dedupe_reagents.values()

  temp_controls = []
  for index, val in enumerate(controls):
    if index != controls.count() - 1 and val.catalog_number != None:
      if val.catalog_number == controls[index + 1].catalog_number and val.name.lower() == controls[index + 1].name.lower():
        temp_controls.append({'name': val.name, 'cat': val.catalog_number})
  dedupe_controls = {str(item): item for item in temp_controls} 
  mergeable_dict['controls'] = dedupe_controls.values()
 
  return mergeable_dict


def send_theshold_alert_email_pcr(request, inventory_alerts):
  mail_subject = f"{request.user.first_name}, PCRprep inventory requires your attention!"
  message = render_to_string('email/pcr_inventory_alert.html', {
    'user': f"{request.user.first_name} {request.user.last_name}",
    'domain': get_current_site(request).domain,
    'inventory': inventory_alerts,
    'protocol': 'https' if request.is_secure() else 'http',
  })
  email = EmailMessage(mail_subject, message, to=[request.user.email])
  email.content_subtype = "html" # this is the crucial part 
  email.send()
 

def send_theshold_alert_email_ext(request, inventory_alerts):
  mail_subject = f"{request.user.first_name}, PCRprep inventory requires your attention!"
  message = render_to_string('email/ext_inventory_alert.html', {
    'user': f"{request.user.first_name} {request.user.last_name}",
    'domain': get_current_site(request).domain,
    'inventory': inventory_alerts,
    'protocol': 'https' if request.is_secure() else 'http',
  })
  email = EmailMessage(mail_subject, message, to=[request.user.email])
  email.content_subtype = "html" # this is the crucial part 
  email.send()