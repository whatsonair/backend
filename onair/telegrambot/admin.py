from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('telegram_chat_id',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('On air', {'fields': ('telegram_chat_id',)}),
    )


admin.site.register(User, UserAdmin)
