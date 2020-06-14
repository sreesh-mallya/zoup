from django.contrib import admin
from django.contrib.auth import get_user_model

from zoup_app import models

admin.site.register(get_user_model())
admin.site.register(models.Menu)
admin.site.register(models.Restaurant)
admin.site.register(models.Item)
admin.site.register(models.Event)
