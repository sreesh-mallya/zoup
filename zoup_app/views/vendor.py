from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from zoup_app.forms.vendor import OwnerForm, RestaurantForm


def partner_with_zoup(request):
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

        return render(request, 'partner-up.html', {'restaurant_form': restaurant_form,
                                                   'owner_form': owner_form
                                                   })


@login_required(login_url='/accounts/sign-in')
@user_passes_test(lambda u: u.account_type == 2)
def all_orders(request):
    return render(request, 'partner/all-orders.html')
