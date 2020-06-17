from django.urls import path

from zoup_app.views import customer, admin, staff, vendor

urlpatterns = [
    path('', customer.index, name='home'),
    path('partner-with-zoup', vendor.partner_with_zoup, name='partner-with-zoup'),
    path('restaurants', customer.restaurant_list, name='restaurant-list'),
    path('restaurants/<str:restaurant_slug>', customer.restaurant_menu, name='restaurant-menu'),
    path('accounts/customer/sign-up', customer.customer_signup, name='customer-sign-up'),
    path('accounts/staff/sign-up', staff.staff_signup, name='staff-sign-up'),
    path('cart', customer.view_cart, name='view-cart'),
    path('orders', customer.view_orders, name='view-orders'),

    # Common account related URLs
    path('accounts/edit-profile', customer.edit_user, name='edit-profile'),
    path('accounts/change-password', customer.change_password, name='change-password'),
    path('accounts/sign-in', customer.user_signin, name='sign-in'),
    path('accounts/sign-out', customer.user_signout, name='sign-out'),

    # Vendor URLs
    path('orders/all', vendor.all_orders, name='partner-all-orders'),
    path('settings', vendor.toggle_serving, name='partner-settings'),

    # Staff URLs
    path('pickups/all', staff.all_pickups, name='staff-all-pickups'),

    # Administration URLs
    path('administration/dashboard/customers', admin.customer_administration, name='admin-customers'),
    path('administration/dashboard/restaurants', admin.restaurant_administration, name='admin-restaurants'),
    path('administration/dashboard/staff', admin.staff_administration, name='admin-staff'),
    path('administration/dashboard/requests', admin.requests_administration, name='admin-requests'),
    path('administration/dashboard/restaurants/<int:restaurant_id>', admin.review_restaurant,
         name='admin-review-restaurant'),
    path('administration/dashboard/restaurants/<int:restaurant_id>/add-item', admin.add_item_to_menu,
         name='admin-add-item'),
    path('administration/dashboard/restaurants/<int:restaurant_id>/menu', admin.view_restaurant_items,
         name='admin-view-items'),
]
