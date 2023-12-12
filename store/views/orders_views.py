from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from users.models import User
from ..models.orders import Order, KitOrder
from ..forms.orders import OrderForm, KitOrderForm


@login_required(login_url='login')
def orders(request):
  orders = Order.objects.filter(user=request.user, has_ordered=True)
  context = {'orders': orders}
  return render(request, 'orders/orders.html', context)


@login_required(login_url='login')
def edit_order(request, username, pk):
  context = {}
  user = User.objects.get(username=username)

  if request.user != user:
    messages.error(request, "There is no order to edit.")
    return redirect('batches')
  
  try:
    order = Order.objects.get(user=user, pk=pk)
  except ObjectDoesNotExist:
    messages.error(request, "There is no order to edit.")
    return redirect('batches')
  
  context = {'order': order}
  return render(request, 'orders/edit_order.html', context)