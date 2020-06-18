from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from zoup_app.constants import ORDER_STATUS
from zoup_app.forms.vendor import OwnerForm, RestaurantForm
from zoup_app.models.vendor import Order


def partner_with_zoup(request):
    """
    Used to create a restaurant partner request. This gets both the owner and restaurant form data from request.POST
    and creates the model instances after validating them. Saves the restaurant first, so that the restaurant's primary
    key can be used to map it to an owner.
    :param request:
    :return:
    """
    if request.method == 'POST':
        owner_form = OwnerForm(request.POST, prefix="owner")
        restaurant_form = RestaurantForm(request.POST, prefix="restaurant")
        if owner_form.is_valid() and restaurant_form.is_valid():
            restaurant = restaurant_form.save()
            owner = owner_form.save(commit=False)
            owner.restaurant = restaurant
            owner.save()
            return render(request, 'partner-up.html', {'success': True})
        else:
            print(owner_form.errors, restaurant_form.errors)
            return render(request, 'partner-up.html', {'restaurant_form': restaurant_form,
                                                       'owner_form': owner_form
                                                       })
    else:
        owner_form = OwnerForm(prefix="owner")
        restaurant_form = RestaurantForm(prefix="restaurant")
        print(restaurant_form)
        return render(request, 'partner-up.html', {'restaurant_form': restaurant_form,
                                                   'owner_form': owner_form
                                                   })


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 2)
def all_orders(request):
    restaurant = request.user.restaurant
    orders = Order.objects.filter(restaurant=restaurant)
    return render(request, 'partner/all-orders.html', {'orders': orders})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 2)
def pending_orders(request):
    restaurant = request.user.restaurant
    orders = Order.objects.filter(restaurant=restaurant, status='pending')
    return render(request, 'partner/pending-orders.html', {'orders': orders})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 2)
def order_history(request):
    restaurant = request.user.restaurant
    orders = Order.objects.filter(
        (Q(status='delivered') | Q(status='picked-up')) & Q(restaurant=restaurant))
    return render(request, 'partner/order-history.html', {'orders': orders})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 2)
def order_details(request, order_id):
    if request.method == 'POST':
        if 'order-status' in request.POST:
            order_status = request.POST['order-status'].lower()
            if order_status in ORDER_STATUS:
                order = Order.objects.get(id=order_id)
                order.status = order_status
                order.save()
                messages.success(request, 'Updated status of order with ID {}.'.format(order_id))
        else:
            messages.success(request, "Oops! Something's wrong. Try again!")
        return redirect('partner-order-details', order_id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id)
        items = order.orderitem_set.all()
        return render(request, 'partner/order-details.html', {'order': order, 'items': items})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 2)
def toggle_serving(request):
    if request.method == 'POST':
        if 'toggle-is-serving' in request.POST:
            value = request.POST['toggle-is-serving'].upper()
            restaurant = request.user.restaurant
            if value == 'TRUE':
                restaurant.is_serving = False
                messages.success(request, 'Status changed.')
            elif value == 'FALSE':
                restaurant.is_serving = True
                messages.success(request, 'Status changed.')
            else:
                messages.error(request, "Oops! Something's wrong. Try again!")
            restaurant.save()
        return redirect('partner-settings')

    else:
        restaurant = request.user.restaurant
        print(restaurant.is_serving)
        return render(request, 'partner/partner-settings.html', {'restaurant': restaurant})
