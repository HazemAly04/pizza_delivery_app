from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Size)
admin.site.register(Sauce)
admin.site.register(Cheese)
admin.site.register(Crust)
admin.site.register(Pizza)
admin.site.register(Order)
admin.site.register(PizzaUser)

