from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AdminProfile, OTP

# Custom admin configuration for the User model
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('full_name', 'email', 'phone_number')
    ordering = ('date_joined',)
    readonly_fields = ('date_joined', 'last_login')

    # Fields displayed on the user detail page
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields displayed on the user creation page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# Admin config for AdminProfile model
@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__full_name', 'user__email', 'user__phone_number')

# Admin config for OTP model
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'code', 'purpose', 'created_at')
    search_fields = ('email', 'phone_number', 'code')
    list_filter = ('purpose', 'created_at')