from .models import Sample, Batch, AssayCode


def create_samples(number_of_samples, lab_id, user):

  batch = Batch.objects.get(lab_id=lab_id)
  
  # create samples for the batch
  for i in range(number_of_samples):

    i += 1
    sample = Sample.objects.create(
      user = user,
      lab_id_num = str(lab_id + "-" + i),
      assay_name = batch.assay_list.name,
      batch = batch,
    )

    sample.assays.add(batch.assay_list.assays.all())

  # create negative control
  control = Sample.objects.create(
    user = user,
    lab_id_numb = str(lab_id + "-" + number_of_samples + 1),
    sample_id = "NegCtrl-Water",
    assay_name = batch.assay_list.name,
    batch = batch,
  )

  control.assays.add(batch.assay_list.assays.all())



  

