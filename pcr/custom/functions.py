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
          sample_data = {
            'position': None,
            'color': colors[color],
            'lab_id': sample.lab_id_num,
            'sample_id': sample.sample_id,
            'assay': assay
          }
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

# compact & organized plate method - horizontal
def compact_organized_horizontal(dna_pcr_samples, process):
  # list plates from smallest to greatest size
  plates = []
  for plate in process.plate.all().order_by('size'):
    plates.append(plate)

  # determine total wells used for samples and controls
  total_wells_used = 0
  for assay_group in dna_pcr_samples:
    for key in assay_group:
      total_wells_used += len(assay_group[key])

  # determine optimal plate size to use
  for plate in plates:
    if plate.size > total_wells_used:
      remaining_wells = plate.size

      # create dictionaries
      plate_data = {'plate': plate}
      protocol_data = {'protocol': process.pcr_dna_protocol}
      samples_data = {'samples': []}
      
      position = 0
      for data in dna_pcr_samples:
        for assay, samples in data.items():
          control_color = samples[0]['color']

          sample_wells = len(samples)
          control_wells = assay.controls.count()
          total_wells = sample_wells + control_wells

          if total_wells < remaining_wells:
              
            for sample in samples:
              position += 1
              sample['position'] = position
              samples_data['samples'].append(sample)
              

            # add validation if plate size is insufficient to even hold only one assay w/ controls
            if plate.size == Plate.Sizes.EIGHT:
              print('plate 8...')
              pass

            if plate.size == Plate.Sizes.FOURTY_EIGHT:
              
              # calculate remaining wells in row by first identifying row that well/position is currently
              wells_in_row = 6
              row = math.floor(position / wells_in_row) + 1
              if position % wells_in_row == 0:
                row -= 1
              rem_wells = (row * wells_in_row) - position

              if control_wells < rem_wells:
                for control in assay.controls.all():
                  position += 1
                  control_data = {
                    'position': position,
                    'color': control_color,
                    'lab_id': control.name,
                    'sample_id': control.lot_number,
                    'assay': assay
                  }
                  samples.append(control_data)
              else:
                # go to next row and add controls there with positions reeee!
                pass

              
        
              pass

            if plate.size == Plate.Sizes.NINETY_SIX:
              pass

            if plate.size == Plate.Sizes.THREE_HUNDRED_EIGHTY_FOUR:
              pass
            


      # remove samples from list that have already been loaded into plate
      for s in samples_data['samples']:
        if s in samples:
          samples.remove(s)

      plate_dict = protocol_data | plate_data | samples_data
   
      break
    else:
      pass

