from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'first_name',
        'last_name',
        'username',
        'bio',
        'email',
        'role',
        'is_active',
        'is_staff'
    )
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'
