from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('User Information', {
            'fields': (
                'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups',
                'last_login', 'date_joined',
            )
        }
        ),
    )
    ordering = ('email',)
    list_display = ('first_name', 'last_name',
                    'email', 'is_staff', 'last_login')
    list_filter = ('is_staff',)
    filter_horizontal = ('groups',)


admin.site.register(User, UserAdmin)
