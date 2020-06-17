from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from zoup_app.constants import ACCOUNT_TYPES, ORDER_STATUS
from zoup_app.forms.user import UserCreationForm
from zoup_app.models.vendor import Order


def staff_signup(request):
    """
    View to handle customer creation via a form. Creates a staff user and sets the corresponding account_type value.
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        messages.info(request, 'Please sign out to register.')
        return render(request, 'staff-signup.html', {})

    if request.method == 'POST':
        staff_form = UserCreationForm(request.POST)
        if staff_form.is_valid():
            user = staff_form.save(commit=False)
            user.account_type = ACCOUNT_TYPES['STAFF']
            user.is_approved = False
            user.save()
            messages.success(request,
                             'Your account has been created. You\'ll be notified when we approve your account.')
            return redirect('sign-in')
        else:
            return render(request, 'staff-signup.html', {'form': staff_form})
    else:
        staff_form = UserCreationForm()
        return render(request, 'staff-signup.html', {'form': staff_form})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 3)
def all_pickups(request):
    orders = Order.objects.filter(customer__location=request.user.location)
    return render(request, 'staff/all-pickups.html', {'orders': orders})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 3)
def pickup_history(request):
    orders = Order.objects.filter(Q(customer__location=request.user.location) & Q(status='delivered'))
    return render(request, 'staff/past-pickups.html', {'orders': orders})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 3)
def pickup_details(request, order_id):
    if request.method == 'POST':
        if 'order-status' in request.POST:
            order_status = request.POST['order-status'].lower()
            if order_status in ORDER_STATUS:
                order = Order.objects.get(id=order_id)
                order.status = order_status
                if order_status == 'delivered':
                    order.delivered_on = timezone.now()
                order.save()
                messages.success(request, 'Updated status of order with ID {}.'.format(order_id))
        else:
            messages.success(request, "Oops! Something's wrong. Try again!")
        return redirect('staff-pickup-details', order_id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id)
        items = order.orderitem_set.all()
        return render(request, 'staff/staff-pickup-details.html', {'order': order, 'items': items})
