from django.contrib.auth.models import Group

def create_premium_group():
  name = "Premium"
  if not Group.objects.filter(name=name).exists():
    Group.objects.create(name=name)
    print("Group: 'Premium' has been created on startup.")