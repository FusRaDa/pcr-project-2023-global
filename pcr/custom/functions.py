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


# order samples by DNA PCR
def dna_pcr_samples(assay_samples): 
  colors = ['table-primary', 'table-secondary', 'table-success', 'table-danger', 'table-warning', 'table-info', 'table-light', 'table-dark']

  # collect all samples that are for DNA in PCR by assay
  all_samples = []
  for index in assay_samples:
    for assay, samples in index.items():
      if assay.method == Assay.Methods.PCR and assay.type == Assay.Types.DNA:
        color = 0
    
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
  pass


def dna_qpcr_samples(assay_samples):
  pass


def rna_qpcr_samples(assay_samples):
  pass


# 4 methods to load plate:
# 1 - compact & organized horizontally
# 2 - compact & organized vertically
# 3 - fully compact horizontally
# 4 - fully compact vertically

def choose_plate(plate_samples, process):
  # add amount validation for plates
  plates = []
  for plate in process.plate.all().order_by('size'):
    plates.append(plate)
  total_wells_used = 0
  for assay_group in plate_samples:
    for assay, samples in assay_group.items():
      total_wells_used += (len(samples) + assay.controls.count())
  for plate in plates:
    if plate.size > total_wells_used:
      return plate
    else:
      return plates[-1]
    

def choose_gel(qpcr_samples, process):
  pass


def organized_horizontal_plate(all_samples, process):
  plate = choose_plate(all_samples, process)

  plate_data = {'plate': choose_plate}
  protocol_data = {'protocol': process.pcr_dna_protocol}
  assays_data = {'assays': []}
  samples_data = {'samples': {}}

  loaded_samples = [] # collect keys to delete later after samples have been added to the json file
  remaining_wells = plate.size
  position = 0

  for data in all_samples:
    for assay, samples in data.items():
      assays_data['assays'].append(assay)
      control_color = samples[1][None]['color']

      sample_wells = len(samples)
      control_wells = assay.controls.count()
      total_wells = sample_wells + control_wells

      if total_wells < remaining_wells: # LOGIC HELP
        for sample in samples:
          position += 1
          sample[f"well{position}"] = sample[None]
          del sample[None]
          loaded_samples.append(sample)
          samples_data['samples'].update(sample)
          
        # add validation if plate size is insufficient to even hold only one assay w/ controls
        if plate.size == Plate.Sizes.EIGHT:
          wells_in_row = 1

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
        rem_wells = (row * wells_in_row) - position

        # if there is enough room in the same row add controls
        if control_wells < rem_wells:

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
              'assay': assay
            }}
            samples_data['samples'].update(control_data)

          remaining_wells = plate.size - block
          # position = block # end of row
        else:
          # go to next row and add controls there with positions reeee!
          pass

      # create plate dictionary that contains plate, tcprotocol, assays, and samples
      plate_dict = protocol_data | plate_data | assays_data | samples_data

      # remove samples from list that have already been loaded into plate
      for sample in loaded_samples:
        samples.remove(sample)

  return plate_dict, all_samples


# compact & organized plate method - horizontal
def json_organized_horizontal_plate(all_samples, process):
  dna_pcr_data = []

  is_empty = False
  while not is_empty:

    plate_dict, all_samples = organized_horizontal_plate(all_samples, process)
    dna_pcr_data.append(plate_dict)

    # check if all samples for each assay is empty if not continue the process of making plates
    for data in all_samples:
      for assay, samples in data.items():
        if len(samples) == 0:
          is_empty = True
        else:
          is_empty = False
  
  return dna_pcr_data
  

