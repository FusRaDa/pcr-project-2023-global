import pytest

from store.custom.functions import generate_order_files

from store.models.affiliates import Brand, Contact
from store.models.items import Tag, Kit, StorePlate, StoreReagent, StoreTube

@pytest.mark.skip
def run():

  brand1 = Brand.objects.create(
    name="BRAND_1",
    is_affiliated = True,
  )

  brand2 = Brand.objects.create(
    name="BRAND_2",
    is_affiliated = False,
  )