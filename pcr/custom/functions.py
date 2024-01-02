from ..models.batch import Batch, Sample


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


def process_dna_pcr_samples():

  data = [] # each plate goes in data 

  plate = {
    'protocol': {
      'name': name,
      'denature': denature,
      'denature_temp': denature_temp,
      'denature_duration': denature_duration,
      'anneal_temp': anneal_temp,
      'anneal_duration': anneal_duration,
      'extension_temp': extension_temp,
      'extension_duration': extension_duration,
      'number_of_cycles': number_of_cycles,
    },

    'samples': [
      {
        'color': color,
        'lab_id': lab_id,
        'sample_id': sample_id,
        'assay': assay
      },

      {
        'color': color,
        'lab_id': lab_id,
        'sample_id': sample_id,
        'assay': assay
      },
      
      {
        'color': color,
        'lab_id': lab_id,
        'sample_id': sample_id,
        'assay': assay
      },
      
    ]
    


  }


  pass


def process_rna_pcr_samples():
  pass


def process_dna_qpcr_samples():
  pass


def process_rna_qpcr_samples():
  pass