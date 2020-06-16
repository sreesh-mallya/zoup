from django import forms
from django.forms import ModelForm

from zoup_app.models import Restaurant
from zoup_app.models.vendor import Owner, Item
from zoup_app.utils import slugify_fields, slugify_field


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        exclude = ('is_approved', 'is_active', 'is_serving', 'banner', 'user')

    def save(self, commit=True):
        restaurant = super().save(commit=False)
        print(restaurant.cuisine)
        restaurant.slug = slugify_fields(restaurant, 'name', 'location')

        if commit:
            restaurant.save()

        return restaurant


class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        exclude = ('restaurant',)

    def clean_name(self):
        name = self.cleaned_data['name']
        if all(x.isalpha() or x.isspace() for x in name):
            return name
        else:
            raise forms.ValidationError('Please enter a valid name. Field must not contain any special characters.')

    def clean_contact(self):
        contact = self.cleaned_data['contact']
        if len(contact) == 10 and contact.isdigit():
            return contact
        else:
            raise forms.ValidationError('Please enter a valid contact number.')


class ItemForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Item
        exclude = ('slug', 'image', 'menu')

    def save(self, commit=True):
        item = super().save()
        item.slug = slugify_field(item, 'name')

        if commit:
            item.save()

        return item
