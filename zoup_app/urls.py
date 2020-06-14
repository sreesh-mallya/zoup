from django.urls import path

from zoup_app.views import auth, admin, staff, vendor

urlpatterns = [
    path('', auth.index, name='home'),
    path('partner-with-zoup', vendor.partner_with_zoup, name='partner-with-zoup'),
    path('administration/dashboard/customers', admin.customer_administration, name='admin-customers'),
    path('administration/dashboard/restaurants', admin.restaurant_administration, name='admin-restaurants'),
    path('administration/dashboard/staff', admin.staff_administration, name='admin-staff'),
    path('administration/dashboard/requests', admin.requests_administration, name='admin-requests'),
    path('administration/dashboard/restaurants/<int:restaurant_id>', admin.review_restaurant,
         name='admin-review-restaurant'),
    path('accounts/edit-profile', auth.edit_user, name='edit-profile'),
    path('accounts/change-password', auth.change_password, name='change-password'),
    path('accounts/sign-in', auth.user_signin, name='sign-in'),
    path('accounts/sign-out', auth.user_signout, name='sign-out'),
    path('accounts/customer/sign-up', auth.customer_signup, name='customer-sign-up'),
    path('accounts/staff/sign-up', staff.staff_signup, name='staff-sign-up'),
    path('orders/all', vendor.all_orders, name='partner-all-orders'),
    path('pickups/all', staff.all_pickups, name='staff-all-pickups'),
]
