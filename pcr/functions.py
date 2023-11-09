from .models import Sample, Batch, AssayCode


def create_samples(number_of_samples, lab_id, user):

  batch = Batch.objects.get(lab_id=lab_id)

  assays = batch.code.assays.all()
  
  # create samples for the batch
  for i in range(number_of_samples):

    i += 1
    sample = Sample.objects.create(
      user = user,
      lab_id_num = lab_id + "-" + str(i),
      assay_name = batch.code.name,
      batch = batch,
    )

    sample.assays.add(*assays)

  # create negative control
  control = Sample.objects.create(
    user = user,
    lab_id_num = lab_id + "-" + str(number_of_samples + 1),
    sample_id = "NegCtrl-Water",
    assay_name = batch.code.name,
    batch = batch,
  )

  control.assays.add(*assays)



  

