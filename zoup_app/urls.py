from django.urls import path

from zoup_app.views import customer, admin, staff, vendor

urlpatterns = [
    path('', customer.index, name='home'),
    path('partner-with-zoup', vendor.partner_with_zoup, name='partner-with-zoup'),
    path('restaurants', customer.restaurant_list, name='restaurant-list'),
    path('events', customer.event_list, name='event-list'),
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
    path('partner/orders/all', vendor.all_orders, name='partner-all-orders'),
    path('partner/orders/pending', vendor.pending_orders, name='partner-pending-orders'),
    path('partner/orders/history', vendor.order_history, name='partner-order-history'),
    path('partner/orders/<int:order_id>', vendor.order_details, name='partner-order-details'),
    path('settings', vendor.toggle_serving, name='partner-settings'),

    # Staff URLs
    path('staff/pickups/all', staff.all_pickups, name='staff-all-pickups'),
    path('staff/pickups/history', staff.pickup_history, name='staff-pickup-history'),
    path('staff/pickups/<int:order_id>', staff.pickup_details, name='staff-pickup-details'),

    # Administration URLs
    path('administration/dashboard/customers', admin.customer_administration, name='admin-customers'),
    path('administration/dashboard/events', admin.view_events, name='admin-events'),
    path('administration/dashboard/events/create', admin.create_event, name='admin-create-event'),
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
