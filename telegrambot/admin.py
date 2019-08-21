from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, NotificationRequest


class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('telegram_chat_id',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('On air', {'fields': ('telegram_chat_id',)}),
    )


class NotificationRequestAdmin(admin.ModelAdmin):
    search_fields = ('request_text', 'user__username')
    list_display = ('user', 'request_text',)
    list_filter = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(NotificationRequest, NotificationRequestAdmin)