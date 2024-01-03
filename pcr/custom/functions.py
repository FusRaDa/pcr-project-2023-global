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


def process_dna_pcr_samples(sample_assays, process): 
  data = [] # each plate goes in data 

  colors = ['table-primary', 'table-secondary', 'table-success', 'table-danger', 'table-warning', 'table-info', 'table-light', 'table-dark']

  all_samples = []
  for index in sample_assays:
    position = 1
    for assay, samples in index.items():
      if assay.method == Assay.Methods.PCR and assay.type == Assay.Types.DNA:
        samples_data = []
        for sample in samples:
          data = {position :{
            'color': None,
            'lab_id': sample.lab_id_num,
            'sample_id': sample.sample_id,
            'assay': assay
          }}
          position += 1
          samples_data.append(data)

        for control in assay.controls.all():
          data = {position :{
            'color': None,
            'lab_id': control.name,
            'sample_id': control.lot_number,
            'assay': assay
          }}
          position += 1
          samples_data.append(data)
        all_samples.append(samples_data)

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



def process_rna_pcr_samples():
  pass


def process_dna_qpcr_samples():
  pass


def process_rna_qpcr_samples():
  pass