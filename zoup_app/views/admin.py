import string
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from zoup_app.constants import ACCOUNT_TYPES
from zoup_app.models import User, Restaurant
from zoup_app.models.vendor import Owner
from zoup_app.utils import string_generator


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def customer_administration(request):
    customers = User.objects.filter(account_type=4)
    return render(request, 'administration/admin-customers.html', {'customers': customers})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def staff_administration(request):
    staff = User.objects.filter(account_type=3)
    return render(request, 'administration/admin-staff.html', {'staff': staff})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def restaurant_administration(request):
    restaurants = Restaurant.objects.filter(is_approved=True)
    return render(request, 'administration/admin-restaurants.html', {'restaurants': restaurants})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def requests_administration(request):
    if request.method == 'POST':
        if 'approve-staff' in request.POST:
            staff_id = request.POST['approve-staff']
            staff = User.objects.get(id=staff_id)
            if staff is None:
                messages.error(request, 'Oops! Couldn\'t complete that action. Try again.')
            else:
                staff.is_approved = True
                staff.save()
                messages.success(request, 'Staff user {} was approved.'.format(staff.name))
        return redirect('admin-requests')

    else:
        staff = User.objects.filter(account_type=3, is_approved=False)
        restaurants = Restaurant.objects.filter(is_approved=False)
        print(restaurants)
        return render(request, 'administration/admin-requests.html', {'staff': staff, 'restaurants': restaurants})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def review_restaurant(request, restaurant_id):
    if request.method == 'POST':
        if 'approve-restaurant' in request.POST:
            restaurant_id = request.POST['approve-restaurant']
            restaurant = Restaurant.objects.get(id=restaurant_id)
            restaurant.is_approved = True

            owner = restaurant.owner
            username = string_generator(size=4, chars=string.digits) + str(int(round(time.time() % 10000)))
            password = string_generator(size=5) + str(int(round(time.time() % 100000)))

            user = User()
            user.username = username
            user.set_password(password)
            user.location = restaurant.location
            user.is_active = True
            user.email = owner.email
            user.contact = owner.contact
            user.name = owner.name
            user.account_type = ACCOUNT_TYPES['RESTAURANT']
            user.is_approved = True
            user.save()

            restaurant.user = user
            restaurant.save()

            messages.success(request,
                             '{}, {} has been approved.'.format(restaurant.name, restaurant.location.capitalize()))
            return render(request, 'administration/admin-restaurant-details.html',
                          {'restaurant': restaurant, 'owner': owner, 'success': True, 'username': username,
                           'password': password})
        return redirect('admin-review-restaurant', restaurant_id=restaurant_id)

    else:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        owner = Owner.objects.get(restaurant=restaurant)
        return render(request, 'administration/admin-restaurant-details.html',
                      {'restaurant': restaurant, 'owner': owner})
