from django.contrib import admin

from .models.affiliates import Brand, Contact
from .models.items import Kit, StorePlate, StoreTube, StoreReagent
from .models.orders import Order, KitOrder
# Register your models here.

models = [
  Brand, Contact,
  Kit, StorePlate, StoreReagent, StoreTube,
  Order, KitOrder,
]

admin.site.register(models)

