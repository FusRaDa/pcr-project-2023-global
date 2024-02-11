from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from users.models import User

# Create your views here.
@staff_member_required(login_url='login')
def dashboard(request):
  users = User.objects.all()

  return render(request, 'dashboard.html')
