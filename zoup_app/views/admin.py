import string
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from zoup_app.constants import ACCOUNT_TYPES
from zoup_app.forms.vendor import ItemForm, EventForm
from zoup_app.models import User, Restaurant
from zoup_app.models.vendor import Owner, Menu, Event
from zoup_app.utils import string_generator


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def customer_administration(request):
    """
    View to show all customers.
    :param request:
    :return:
    """
    customers = User.objects.filter(account_type=4)
    return render(request, 'administration/admin-customers.html', {'customers': customers})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def staff_administration(request):
    """
    View to show all approved staff.
    :param request:
    :return:
    """
    staff = User.objects.filter(account_type=3, is_approved=True)
    return render(request, 'administration/admin-staff.html', {'staff': staff})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def restaurant_administration(request):
    """
    View to show all approved restaurants.
    :param request:
    :return:
    """
    restaurants = Restaurant.objects.filter(is_approved=True)
    return render(request, 'administration/admin-restaurants.html', {'restaurants': restaurants})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def requests_administration(request):
    """
    View to show staff and restaurants that are pending approval. For restaurants, the requests need to be reviewed
    first from the details page. This view checks for `approve-staff` in request.POST, which would be the name of the
    hidden input field to approve staff, and the value passed from the hidden field would be used to find the staff
    and change the status.
    :param request:
    :return:
    """
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
    """
    Approve a restaurant, based on the form hidden input field value, which would be 'approve-restaurant', having the
    value set to the restaurant's ID. The restaurant's owner is queried using a reverse relationship, and a user is
    created with the owner's attributes. A randomly generated numeric username is also assigned, along with a password.
    These credentials will be used by the restaurant owner to sign in and manage orders.
    :param request:
    :param restaurant_id:
    :return:
    """
    if request.method == 'POST':
        if 'approve-restaurant' in request.POST:
            restaurant_id = request.POST['approve-restaurant']
            restaurant = Restaurant.objects.get(id=restaurant_id)
            restaurant.is_approved = True

            # Create a menu for the restaurant
            menu = Menu(restaurant=restaurant)
            menu.save()

            owner = restaurant.owner

            # Generate username and password from custom string generator utility function
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


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def add_item_to_menu(request, restaurant_id):
    """
    This view is used to add an item to a restaurant's menu. Uses a Item model form to get Item details and validate
    them. If a restaurant doesn't have a menu object (reverse access to the restaurant OneToOneField), a menu is created
    and the restaurant field is set to the restaurant being accessed based on the `restaurant_id` path parameter.
    :param request:
    :param restaurant_id: ID of the restaurant to whose menu needs an item added
    :return:
    """
    if request.method == 'POST':
        restaurant = Restaurant.objects.get(id=restaurant_id)
        item_form = ItemForm(request.POST)
        print(item_form.as_p())

        # Get the restaurant's menu, or create one if it doesn't exist
        try:
            menu = restaurant.menu
        except Menu.DoesNotExist:
            menu = Menu(restaurant=restaurant)
            menu.save()

        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.menu = menu  # Add item to the restaurant's menu
            item.save()
            messages.success(request, "Item {} added to {}'s menu.".format(item.name, restaurant.name))

        return redirect('admin-add-item', restaurant_id=restaurant_id)

    else:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        item_form = ItemForm()

        return render(request, 'administration/restaurant-add-item.html', {'form': item_form, 'restaurant': restaurant})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def view_restaurant_items(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    items = restaurant.menu.item_set.all()
    return render(request, 'administration/restaurant-view-items.html', {'items': items, 'restaurant': restaurant})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def view_events(request):
    events = Event.objects.all()
    return render(request, 'administration/admin-events.html', {'events': events})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 1)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-events')
        else:
            return render(request, 'administration/create-event.html', {'form': form})
    else:
        form = EventForm()
        return render(request, 'administration/create-event.html', {'form': form})
