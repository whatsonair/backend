from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, NotificationRequest, RadioStation, Playlist


class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('telegram_chat_id',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('On air', {'fields': ('telegram_chat_id',)}),
    )


class NotificationRequestAdmin(admin.ModelAdmin):
    search_fields = ('request_text', 'user__username')
    list_display = ('user', 'request_text',)
    list_filter = ('user',)


class RadioStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'monitor', 'scrapper_set')
    list_filter = ('monitor',)
    search_fields = ('name', 'url')


class PlaylistAdmin(admin.ModelAdmin):
    search_fields = ('on_air', 'station__name')
    list_display = ('time', 'station', 'on_air',)
    list_filter = ('station__name',)


admin.site.register(User, UserAdmin)
admin.site.register(NotificationRequest, NotificationRequestAdmin)
admin.site.register(RadioStation, RadioStationAdmin)
admin.site.register(Playlist, PlaylistAdmin)
