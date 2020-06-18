from django.db import models

from zoup_app.constants import LOCATIONS, CUISINES, ITEM_TYPES, ORDER_STATUS_CHOICES, PAYMENT_TYPE_CHOICES, \
    PAYMENT_STATUS_CHOICES, ITEM_CATEGORY
from zoup_app.models import User


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=100, blank=False)
    banner = models.URLField(blank=True, null=True)
    license_number = models.CharField(max_length=15, blank=False)
    pan_or_gstin = models.CharField(max_length=15, blank=False)
    fssai = models.CharField(max_length=14, blank=False)
    location = models.CharField(max_length=50, choices=LOCATIONS)
    is_serving = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True)
    cuisine = models.CharField(max_length=50, choices=CUISINES, null=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    support_delivery = models.BooleanField(default=True)

    def __str__(self):
        return '{}, {}'.format(self.name, self.location.capitalize())


class Owner(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    contact = models.CharField(max_length=10, blank=False)
    email = models.EmailField(blank=False)

    def __str__(self):
        return '{} : {}'.format(self.name, self.restaurant.name)


class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return 'Menu for {}'.format(self.restaurant.name)


class Item(models.Model):
    name = models.CharField(max_length=100, blank=False)
    price = models.IntegerField(blank=False)
    slug = models.SlugField(blank=True)
    image = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50, choices=ITEM_TYPES)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    category = models.CharField(choices=ITEM_CATEGORY, max_length=50)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100, blank=False)
    venue = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=None, null=True)
    description = models.CharField(max_length=1000, blank=False)
    from_date = models.DateField(blank=True)
    to_date = models.DateField(blank=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    item_count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, null=True, default=None, blank=True)

    def __str__(self):
        return "{}'s cart - {} item(s) - Total: {}".format(self.user.username, self.item_count, self.total)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    staff = models.ForeignKey(User, on_delete=models.SET(None), null=True, related_name='staff_orders')
    item_count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET(None), null=True)
    delivered_on = models.DateTimeField(null=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, default='pending', max_length=20)
    payment_type = models.CharField(choices=PAYMENT_TYPE_CHOICES, default='cash-on-delivery', max_length=50,
                                    blank=False)
    payment_status = models.CharField(choices=PAYMENT_STATUS_CHOICES, default='pending', max_length=20, blank=False)

    def __str__(self):
        return '{} - {} - {}'.format(self.restaurant.name, self.customer.username, self.total)


class Pickup(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {} - {}'.format(self.staff.name, self.order.id, self.order.restaurant.name)


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET(None), null=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.item, self.quantity)


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET(None), null=True, default=None)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.item, self.quantity)
