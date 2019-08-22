import importlib
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, NotificationRequest, RadioStation, Scrapper


class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('telegram_chat_id',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('On air', {'fields': ('telegram_chat_id',)}),
    )


class NotificationRequestAdmin(admin.ModelAdmin):
    search_fields = ('request_text', 'user__username')
    list_display = ('user', 'request_text',)
    list_filter = ('user',)


class ScrapperInline(admin.TabularInline):
    model = Scrapper
    fields = ('python_path', 'priority', 'used', 'success_rate')
    readonly_fields = ('used', 'success_rate',)
    ordering = ('priority',)
    extra = True


class RadioStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'monitor')
    list_filter = ('monitor',)
    inlines = [
        ScrapperInline,
    ]


class ScrapperAdmin(admin.ModelAdmin):
    search_fields = ('radio__name', 'python_path')
    list_display = ('radio', 'python_path', 'priority', 'used', 'success_rate',)
    actions = ['trigger']

    def trigger(self, request, queryset):
        for scrapper in queryset:
            try:
                function_string = scrapper.python_path
                mod_name, func_name = function_string.rsplit('.', 1)
                mod = importlib.import_module(mod_name)
                func = getattr(mod, func_name)
                result = func()
                self.message_user(request, '{}: {}'.format(scrapper, result))
            except Exception as exc:
                self.message_user(request, '{}: {}: {}'.format(scrapper, type(exc).__name__, exc), messages.ERROR)
    trigger.short_description = 'Trigger scrapper'


admin.site.register(User, UserAdmin)
admin.site.register(NotificationRequest, NotificationRequestAdmin)
admin.site.register(RadioStation, RadioStationAdmin)
admin.site.register(Scrapper, ScrapperAdmin)
