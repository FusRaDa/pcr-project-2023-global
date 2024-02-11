from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

from .models import LoginAction, UserGroup

def record_user_login(user):  
  try:
    LoginAction.objects.get(user=user, date=now().date())
  except ObjectDoesNotExist:
    login_action = LoginAction.objects.create(user=user)

    try:
      user_group = UserGroup.objects.get(date=now())
      user_group.users.add(login_action)
    except ObjectDoesNotExist:
      user_group = UserGroup.objects.create(date=now())
      user_group.users.add(login_action)

  


  