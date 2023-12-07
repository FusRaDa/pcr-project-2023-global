from django.db import models
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from ..models.items import Kit


class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  kit = models.ForeignKey(Kit, on_delete=models.SET_NULL)

  amount = models.IntegerField(validators=[MinValueValidator(0)], default=1)

  date_added = models.DateTimeField(default=now, editable=False)
  has_ordered = models.BooleanField(blank=False, default=False)




  