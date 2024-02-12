from django.db import models
from django.utils.timezone import now

from users.models import User


class LoginList(models.Model):
  date = models.DateField(default=now, editable=False, unique=True)

  @property
  def date_str(self):
    return self.date.strftime('%m-%d-%Y')

  @property
  def logins(self):
    return self.loginaction_set.count()
  
  def __str__(self):
    return self.date


class LoginAction(models.Model):
  list = models.ForeignKey(LoginList, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateField(default=now, editable=False)

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['list', 'user', 'date'], 
        name='login_action_unique',
        violation_error_message = "A login action already exists!"
      )
    ]

  def __str__(self):
    return f'{self.user}-{self.date}'


