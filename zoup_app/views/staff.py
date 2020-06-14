from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from zoup_app.constants import ACCOUNT_TYPES
from zoup_app.forms.user import UserCreationForm


def staff_signup(request):
    """
    View to handle customer creation via a form.
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
    return render(request, 'staff/all-pickups.html')
