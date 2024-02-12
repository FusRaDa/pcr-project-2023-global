from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

from .models import LoginAction, LoginList

def record_user_login(user):  
  try:
    user_list = LoginList.objects.get(date=now())
  except ObjectDoesNotExist:
    user_list = LoginList.objects.create(date=now())

  try: 
    LoginAction.objects.get(list=user_list, user=user, date=now().date())
  except ObjectDoesNotExist:
    LoginAction.objects.create(list=user_list, user=user, date=now().date())