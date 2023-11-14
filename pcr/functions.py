from django.core.exceptions import ValidationError
from .models import *


BATCH_LIMIT = 5

def create_samples(number_of_samples, lab_id, user):

  batch = Batch.objects.get(lab_id=lab_id)

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
    lab_id_num = lab_id + "-" + str(number_of_samples + 1),
    sample_id = "NegCtrl-Water",
    batch = batch,
  )

  control.assays.add(*assays)


def limit_batch_count(user):
  num = Batch.objects.filter(user=user).count() + 1
  if num > BATCH_LIMIT:
    print('limit reached')
    raise ValidationError(
      message="You have reached the number of batches you can create."
    )


  

