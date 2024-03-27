from django.contrib import admin

# Register your models here.
from django.contrib import admin
from notifications.models import Notification

admin.site.register(Notification)
