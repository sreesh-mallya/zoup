from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from zoup_app.constants import ACCOUNT_TYPES
from zoup_app.forms.user import UserCreationForm, UserChangeForm, UserPasswordChangeForm
from zoup_app.models import Restaurant, Item
from zoup_app.models.vendor import Cart, CartItem


def index(request):
    return render(request, 'index.html', {})


def customer_signup(request):
    """
    View to handle customer creation via a form. Create a customer user, and assign the corresponding account_type value.
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        messages.info(request, 'Please sign out to register.')
        return render(request, 'customer-signup.html', {})

    if request.method == 'POST':
        customer_form = UserCreationForm(request.POST)
        if customer_form.is_valid():
            user = customer_form.save(commit=False)
            user.account_type = ACCOUNT_TYPES['CUSTOMER']
            user.save()
            messages.success(request, 'Your account has been created.')
            return redirect('sign-in')
        else:
            return render(request, 'customer-signup.html', {'form': customer_form})
    else:
        customer_form = UserCreationForm()
        print(customer_form)
        return render(request, 'customer-signup.html', {'form': customer_form})


@login_required(login_url='/accounts/sign-in')
def edit_user(request):
    """
    View to handle user edit via a form. Uses django's model form to directly update values, since the instance of
    request.user, which would correspond to the user who's logged in. Only customers or staff can access this page.
    :param request:
    :return:
    """
    if request.method == 'POST':
        edit_user_form = UserChangeForm(request.POST, instance=request.user)
        if edit_user_form.is_valid():
            user = edit_user_form.save()
            messages.success(request, 'Your changes have been saved.')
            return redirect('edit-profile')
        else:
            return render(request, 'edit-profile.html', {'form': edit_user_form})
    else:
        edit_user_form = UserChangeForm(instance=request.user)
        return render(request, 'edit-profile.html', {'form': edit_user_form})


def user_signin(request):
    """
    Handle sign in requests for all user types, and redirect them to the respective pages.
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            print(user)
            if (user.is_active and (user.account_type == 4 or user.account_type == 1)) or \
                    (user.is_active and user.is_approved and (user.account_type == 3 or user.account_type == 2)):
                login(request, user)

                if user.account_type == 1:
                    return redirect('admin-customers')
                elif user.account_type == 2:
                    return redirect('partner-all-orders')
                elif user.account_type == 3:
                    return redirect('staff-all-pickups')
                elif user.account_type == 4:
                    return redirect('home')  # TODO: Implement redirection
                else:
                    return redirect('home')
            elif not user.is_approved and user.account_type == 3 or user.account_type == 2:
                messages.error(request,
                               'This user has not yet been approved. '
                               'You\'ll be notified when your account has been approved.')
            else:
                messages.error(request, 'This user has been deactivated.')

        else:
            messages.error(request, 'Invalid username and password combination.')

        return render(request, 'signin.html', {
            'invalid_login': True,
        })

    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'signin.html')


@login_required(login_url='/accounts/sign-in')
def user_signout(request):
    """
    Log out a logged in user.
    """
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/accounts/sign-in')
def change_password(request):
    """
    View that handles password change. This uses a UserPasswordChangeForm, that inherits from Django's built in
    PasswordChangeForm to modify form input field attributes.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was updated.')
            return redirect('change-password')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = UserPasswordChangeForm(request.user)

    return render(request, 'change-password.html', {'form': form})


def restaurant_list(request):
    restaurants = Restaurant.objects.filter(is_approved=True)
    return render(request, 'restaurant-list.html', {'restaurants': restaurants})


def restaurant_menu(request, restaurant_slug):
    if request.method == 'POST' and request.user.is_authenticated:
        restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
        if 'item-id' in request.POST and 'item-quantity' in request.POST:
            item_id = request.POST['item-id']
            item_quantity = request.POST['item-quantity']
            item = Item.objects.get(id=item_id)
            try:
                cart = request.user.cart
            except Cart.DoesNotExist:
                cart = Cart(user=request.user, restaurant=restaurant)
                cart.save()
            cart_item = CartItem(cart=cart, item=item, quantity=item_quantity)
            cart_item.save()

    else:
        restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
        items = restaurant.menu.item_set.all()
        return render(request, 'restaurant-menu.html', {'restaurant': restaurant, 'items': items})


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == ACCOUNT_TYPES['CUSTOMER'])
def view_cart(request):
    pass
