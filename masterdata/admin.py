from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(CusztomFCMDevice)
admin.site.register(NotificationData)

admin.site.register(PublicUrl)