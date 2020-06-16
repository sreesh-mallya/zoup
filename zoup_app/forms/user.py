from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm

from zoup_app.constants import LOCATIONS


class UserCreationForm(ModelForm):
    """
    Form class for creating Customers and Staff since they contain the same fields.
    The functions in this class validate data and first create a User object, and then maps that User object to the
    Customer object and save them in the database.
    """
    # Form fields for creating Customers or Staff

    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'autofocus': 'true',
            'class': 'form-control',
            'placeholder': 'Username'
        }
    ), required=True)

    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }
    ), required=True)

    name = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Name'
        }
    ), required=True)

    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }
    ), required=True)

    contact = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contact',
            'maxlength': '10'
        }
    ), required=True)

    location = forms.CharField(label='Select your location', widget=forms.Select(
        choices=LOCATIONS,
        attrs={
            'class': 'form-control',
            'placeholder': 'Location'
        }
    ))

    # Automatically create form fields from model fields
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'name', 'email', 'contact', 'location']

    # Check name for special characters
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

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on the user,
    except for certain fields like the username and password.
    """
    name = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Name'
        }
    ), required=True)

    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }
    ), required=True)

    contact = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contact',
            'maxlength': '10'
        }
    ), required=True)

    location = forms.CharField(label='Select your location', widget=forms.Select(
        choices=LOCATIONS,
        attrs={
            'class': 'form-control',
            'placeholder': 'Location'
        }
    ))

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'contact', 'location')

    # Check name for special characters
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


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Old Password'
            }
        ),
    )

    new_password1 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New Password'
            }
        ),
    )

    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New Password'
            }
        ),
    )
