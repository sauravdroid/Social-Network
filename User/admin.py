from django.contrib import admin
from . models import CustomUser,ProfileCustomer
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ProfileCustomer)
