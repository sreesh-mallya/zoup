from django.db import models

from zoup_app.constants import LOCATIONS, CUISINES, ITEM_TYPES
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
    cuisines = models.CharField(max_length=50, choices=CUISINES)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    support_delivery = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Owner(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    contact = models.CharField(max_length=10, blank=False)
    email = models.EmailField(blank=False)

    def __str__(self):
        return '{} : {}'.format(self.name, self.restaurant.name)


class Item(models.Model):
    name = models.CharField(max_length=100, blank=False)
    price = models.IntegerField(blank=False)
    slug = models.SlugField(blank=True)
    image = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=False)
    type = models.CharField(max_length=50, choices=ITEM_TYPES)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, primary_key=True)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return 'Menu for {}'.format(self.restaurant.name)


class Event(models.Model):
    name = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(blank=True)
    banner = models.URLField(blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=False)
    description = models.CharField(max_length=1000, blank=False)
    from_date = models.DateTimeField(blank=True)
    to_date = models.DateTimeField(blank=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
