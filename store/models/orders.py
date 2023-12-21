from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal

from users.models import User
from ..models.items import Kit


# one order can only have on kit/product 
class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  kits = models.ManyToManyField(Kit, through='KitOrder')

  has_ordered = models.BooleanField(blank=False, default=False)
  date_processed = models.DateTimeField(blank=True, null=True, editable=False, default=None)

  orders_file = models.FileField(null=True, blank=True, upload_to='orders')

  @property
  def total_cost(self):
    cost = 0
    amounts = self.kitorder_set.all()
    for amount in amounts:
      cost += Decimal(amount.kit.price * amount.amount_ordered)
    return cost

  @property
  def date_format(self):
    # look into https://pypi.org/project/django-tz-detect/ for turning UTC into user local timezone!
    return self.date_processed.strftime("%Y/%m/%d at %I:%M %p")
  
  @property
  def date_file(self):
    return self.date_processed.strftime("%Y_%m_%d")
  
  def __str__(self):
    return f"Order by: {self.user}"
  

class KitOrder(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  kit = models.ForeignKey(Kit, on_delete=models.CASCADE)

  amount_ordered = models.IntegerField(validators=[MinValueValidator(1)], default=1)
  remaining_transfers = models.IntegerField(validators=[MinValueValidator(0)], default=0)

  def __str__(self):
    return f"Through - {self.kit.name}"