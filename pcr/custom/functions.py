from ..models.batch import Batch, Sample
from ..models.assay import Assay
from ..models.inventory import Plate
import math


def create_samples(number_of_samples, lab_id, user):
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

  # create negative control
  control = Sample.objects.create(
    user = user,
    lab_id_num = lab_id + "-" + str(number_of_samples + 1) + " (NC)",
    sample_id = "NegCtrl-Water",
    batch = batch,
  )

  control.assays.add(*assays)


# order ALL samples by assay
def samples_by_assay(samples):
  all_assays = []
  for sample in samples:
    for assay in sample.assays.all():
      all_assays.append(assay)
  assays = list(set(all_assays))
  
  assay_samples = []
  for assay in assays:
    x = {assay:[]}
    for sample in samples:
      if sample.assays.contains(assay):
        x[assay].append(sample)
    assay_samples.append(x)
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


def choose_plate(all_samples, plates):
  total_wells_used= 0
  for assay_group in all_samples:
    for assay, samples in assay_group.items():
      total_wells_used += (len(samples) + assay.controls.count())

  chosen_plate = None     
  for plate in plates:
    if plate[0].size >= total_wells_used and plate[1] > 0:
      plate[1] -= 1
      chosen_plate = plate[0]

  if chosen_plate == None:
    for plate in plates.reverse():
      if plate[1] > 0:
        plate[1] -= 1
        chosen_plate = plate[0]

  plates.reverse()
  return chosen_plate, plates
 
    

def choose_gel(all_samples, process):
  gels = []
  for gel in process.gel.all().order_by('size'):
    gels.append(gel)
  total_wells_used = 0
  for assay_group in all_samples:
    for assay, samples in assay_group.items():
      total_wells_used += (len(samples) + assay.controls.count())
  for gel in gels:
    if gel.size > total_wells_used:
      return gel
    else:
      return gels[-1]


def load_plate(all_samples, process, protocol, minimum_samples_in_plate):
  plate = choose_plate(all_samples, process)

  plate_data = {'size': plate.size}
  protocol_data = {'protocol': {
    'name': protocol.name,
    'denature_temp': float(protocol.denature_temp),
    'denature_duration': protocol.denature_duration,
    'anneal_temp': float(protocol.anneal_temp),
    'anneal_duration': protocol.anneal_duration,
    'extension_temp': float(protocol.extension_temp),
    'extension_duration': protocol.extension_duration,
    'number_of_cycles': protocol.number_of_cycles
  }}
  assays_data = {'assays': []}
  samples_data = {'samples': {}}

  remaining_wells = plate.size
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
            'sample_volume': float(assay.sample_volume),
            'reaction_volume': float(assay.reaction_volume),
            'mm_volume': float(assay.mm_volume),
            'reagents': [],
          }
          
          for reagent in assay.reagentassay_set.all().order_by('order'):
            stock_concentration = None
            if reagent.reagent.stock_concentration:
              stock_concentration = float(reagent.reagent.stock_concentration)

            final_stock_concentration = None
            if reagent.final_concentration:
              final_stock_concentration = float(reagent.final_concentration)

            dilution_factor = None
            if reagent.dilution_factor:
              dilution_factor = float(reagent.dilution_factor)

            assay_dict['reagents'].append({
              'name': reagent.reagent.name,
              'volume_per_sample': float(reagent.volume_per_sample),
              'stock_concentration': stock_concentration,
              'unit_concentration': reagent.reagent.unit_concentration,
              'final_stock_concentration': final_stock_concentration,
              'final_unit_concentration': reagent.final_concentration_unit,
              'dilution_factor': dilution_factor,
            })
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
          rem_wells_in_row = (row * wells_in_row) - position + 1

          # if there is enough room in the same row add controls
          if control_wells < rem_wells_in_row:
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

            remaining_wells -= block
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

              remaining_wells -= block
              position = block
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
        # if assay samples wont fit in remaining wells... (total wells > remaining_wells)
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
              'sample_volume': float(assay.sample_volume),
              'reaction_volume': float(assay.reaction_volume),
              'mm_volume': float(assay.mm_volume),
              'reagents': [],
            }
            
            for reagent in assay.reagentassay_set.all().order_by('order'):
              stock_concentration = None
              if reagent.reagent.stock_concentration:
                stock_concentration = float(reagent.reagent.stock_concentration)

              final_stock_concentration = None
              if reagent.final_concentration:
                final_stock_concentration = float(reagent.final_concentration)

              dilution_factor = None
              if reagent.dilution_factor:
                dilution_factor = float(reagent.dilution_factor)

              assay_dict['reagents'].append({
                'name': reagent.reagent.name,
                'volume_per_sample': float(reagent.volume_per_sample),
                'stock_concentration': stock_concentration,
                'unit_concentration': reagent.reagent.unit_concentration,
                'final_stock_concentration': final_stock_concentration,
                'final_unit_concentration': reagent.final_concentration_unit,
                'dilution_factor': dilution_factor,
              })
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

  # create plate dictionary that contains plate, tcprotocol, assays, and samples
  plate_dict = protocol_data | plate_data | assays_data | samples_data
  return plate_dict, all_samples, plate


def load_gel(all_samples, process, protocol, minimum_samples_in_gel):
  gel = choose_gel(all_samples, process)

  gel_data = {'size': gel.size}
  protocol_data = {'protocol': {
    'name': protocol.name,
    'denature_temp': float(protocol.denature_temp),
    'denature_duration': protocol.denature_duration,
    'anneal_temp': float(protocol.anneal_temp),
    'anneal_duration': protocol.anneal_duration,
    'extension_temp': float(protocol.extension_temp),
    'extension_duration': protocol.extension_duration,
    'number_of_cycles': protocol.number_of_cycles
  }}
  assays_data = {'assays': []}
  samples_data = {'samples': {}}

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
          
          assay_dict = {
            'name': assay.name,
            'sample_num': num_samples + control_wells,
            'sample_volume': float(assay.sample_volume),
            'reaction_volume': float(assay.reaction_volume),
            'mm_volume': float(assay.mm_volume),
            'reagents': [],
          }
          
          for reagent in assay.reagentassay_set.all().order_by('order'):
            stock_concentration = None
            if reagent.reagent.stock_concentration:
              stock_concentration = float(reagent.reagent.stock_concentration)

            final_stock_concentration = None
            if reagent.final_concentration:
              final_stock_concentration = float(reagent.final_concentration)

            dilution_factor = None
            if reagent.dilution_factor:
              dilution_factor = float(reagent.dilution_factor)

            assay_dict['reagents'].append({
              'name': reagent.reagent.name,
              'volume_per_sample': float(reagent.volume_per_sample),
              'stock_concentration': stock_concentration,
              'unit_concentration': reagent.reagent.unit_concentration,
              'final_stock_concentration': final_stock_concentration,
              'final_unit_concentration': reagent.final_concentration_unit,
              'dilution_factor': dilution_factor,
            })
          assays_data['assays'].append(assay_dict)

          for control in assay.controlassay_set.all().order_by('order'):
            position += 1
            control_data = {f"well{position}": {
              'color': control_color,
              'lab_id': control.control.name,
              'sample_id':control.control.lot_number,
              'assay': assay.name
            }}
            samples_data['samples'].update(control_data)
          
          position += 1
          ladder = {f"well{position}": {
              'color': control_color,
              'lab_id': 'LADDER LAB_ID',
              'sample_id': 'LADDER SAMPLE_ID',
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
            
            assay_dict = {
              'name': assay.name,
              'sample_num': num_samples + control_wells,
              'sample_volume': float(assay.sample_volume),
              'reaction_volume': float(assay.reaction_volume),
              'mm_volume': float(assay.mm_volume),
              'reagents': [],
            }
          
            for reagent in assay.reagentassay_set.all().order_by('order'):
              stock_concentration = None
              if reagent.reagent.stock_concentration:
                stock_concentration = float(reagent.reagent.stock_concentration)

              final_stock_concentration = None
              if reagent.final_concentration:
                final_stock_concentration = float(reagent.final_concentration)

              dilution_factor = None
              if reagent.dilution_factor:
                dilution_factor = float(reagent.dilution_factor)

              assay_dict['reagents'].append({
                'name': reagent.reagent.name,
                'volume_per_sample': float(reagent.volume_per_sample),
                'stock_concentration': stock_concentration,
                'unit_concentration': reagent.reagent.unit_concentration,
                'final_stock_concentration': final_stock_concentration,
                'final_unit_concentration': reagent.final_concentration_unit,
                'dilution_factor': dilution_factor,
              })
            assays_data['assays'].append(assay_dict)

            for control in assay.controlassay_set.all().order_by('order'):
              position += 1
              control_data = {f"well{position}": {
                'color': control_color,
                'lab_id': control.control.name,
                'sample_id':control.control.lot_number,
                'assay': assay.name
              }}
              samples_data['samples'].update(control_data)
            
            position += 1
            ladder = {f"well{position}": {
                'color': control_color,
                'lab_id': assay.ladder.name,
                'sample_id': assay.ladder.lot_number,
                'assay': assay.name
              }}
            samples_data['samples'].update(ladder)
            remaining_wells = 0
          else:
            remaining_wells = 0
        
        for sample in loaded_samples:
          samples.remove(sample)
     
  gel_dict = protocol_data | gel_data | assays_data | samples_data
  return gel_dict, all_samples, gel


def process_qpcr_samples(all_samples, process, protocol, minimum_samples_in_plate):
  qpcr_data = []

  #### MANAGE INVENTORY HERE ####
  plates = []
  for plate in process.plate.all().order_by('size'):
    plates.append([plate, plate.amount])

  is_empty = False
  while not is_empty:
 
    plate_dict, all_samples, plate = load_plate(all_samples, process, protocol, minimum_samples_in_plate)
    qpcr_data.append(plate_dict)

    # check if all samples for each assay is empty if not continue the process of making plates
    for data in all_samples:
      for assay, samples in data.items():
        if len(samples) == 0:
          is_empty = True
        else:
          is_empty = False
  
  return qpcr_data, plates


def process_pcr_samples(all_samples, process, protocol, minimum_samples_in_gel):
  pcr_data = []
  inventory = []

  #### MANAGE INVENTORY HERE ####
  
  is_empty = False
  while not is_empty:

    gel_dict, all_samples, gel = load_gel(all_samples, process, protocol, minimum_samples_in_gel)
    pcr_data.append(gel_dict)
    inventory.append(gel)

    for data in all_samples:
      for assay, samples in data.items():
        if len(samples) == 0:
          is_empty = True
        else:
          is_empty = False
    
  return pcr_data, inventory

