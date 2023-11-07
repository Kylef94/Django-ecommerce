from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import  *

class CustomerAdmin(UserAdmin):
    model = Customer
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    ordering = ('email',)
    
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name",
                )}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "fields": (
                "email", "password", "first_name", "last_name",
                "is_active", "is_staff",
            )}
        ),
    )
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address)