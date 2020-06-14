from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _

from zoup_app.constants import LOCATIONS


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('email should have a value assigned!')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('account_type', 0)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom 'User' model. All the authentication for the app will be handled with this model.
    """

    USER_TYPE_CHOICES = (
        (0, 'superuser'),
        (1, 'admin'),
        (2, 'restaurant'),
        (3, 'staff'),
        (4, 'customer'),
    )

    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$',
                                                              _('Enter a valid username. '
                                                                'This value may contain only letters, numbers '
                                                                'and @/./+/-/_ characters.'), 'invalid'),
                                ],
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                                })

    date_joined = models.DateField(auto_now_add=True)

    account_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=4)

    contact = models.CharField(max_length=10, blank=False)

    name = models.CharField(max_length=100, blank=False)

    email = models.EmailField(unique=True, null=False, error_messages={
        'unique': _("A user with that email already exists."),
    })

    location = models.CharField(max_length=100, choices=LOCATIONS, blank=False)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    is_approved = models.BooleanField(_('approved'), default=False)

    is_available = models.BooleanField(_('available'), default=True)

    USERNAME_FIELD = 'username'

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
