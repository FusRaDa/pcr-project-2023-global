from django.db import models
from django.utils.timezone import now

from users.models import User


class LoginAction(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateField(default=now().date(), editable=False)

  def __str__(self):
    return f'{self.user}-{self.date}'
  

class UserGroup(models.Model):
  date = models.DateField(default=now().date(), editable=False)
  users = models.ManyToManyField(LoginAction)

  def __str__(self):
    return self.date

