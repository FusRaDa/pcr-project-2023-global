from ..models.batch import Batch, Sample
from ..models.assay import Assay


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
def dna_pcr_samples_by_assay(assay_samples): 
  colors = ['table-primary', 'table-secondary', 'table-success', 'table-danger', 'table-warning', 'table-info', 'table-light', 'table-dark']

  # collect all samples that are for DNA in PCR by assay
  dna_pcr_samples = []
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
        dna_pcr_samples.append(assay_data)

  return dna_pcr_samples


# compact plate method
def json_dna_pcr(dna_pcr_samples, process):
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

      plate_data = {'plate': plate}
      protocol_data = {'protocol': process.pcr_dna_protocol}
      samples_data = {'samples': []}
      
      position = 1
      for data in dna_pcr_samples:
        for assay, samples in data.items():
          control_color = samples[0]['color']
       
          for sample in samples:
            sample['position'] = position
            samples_data['samples'].append(sample)

            position += 1
            remaining_wells -= 1

          for s in samples_data['samples']:
            if s in samples:
              samples.remove(s)
          
          # if len(samples) > 0:
          #   for control in assay.controls.all():
          #     control_data = {
          #       'position': None,
          #       'color': control_color,
          #       'lab_id': control.name,
          #       'sample_id': control.lot_number,
          #       'assay': assay
          #     }
          #     samples.append(control_data)

      plate_dict = protocol_data | plate_data | samples_data
   
      break
    else:
      pass

 
  
 
 



  
 
     

  

  
  
      
    
  







  



  


 

  # plate = {
  #   'protocol': {
  #     'name': name,
  #     'denature': denature,
  #     'denature_temp': denature_temp,
  #     'denature_duration': denature_duration,
  #     'anneal_temp': anneal_temp,
  #     'anneal_duration': anneal_duration,
  #     'extension_temp': extension_temp,
  #     'extension_duration': extension_duration,
  #     'number_of_cycles': number_of_cycles,
  #   },

  #   'samples': [
  #     {
  #       'color': color,
  #       'lab_id': lab_id,
  #       'sample_id': sample_id,
  #       'assay': assay
  #     },

  #     {
  #       'color': color,
  #       'lab_id': lab_id,
  #       'sample_id': sample_id,
  #       'assay': assay
  #     },
      
  #     {
  #       'color': color,
  #       'lab_id': lab_id,
  #       'sample_id': sample_id,
  #       'assay': assay
  #     },
      
  #   ]
  # }