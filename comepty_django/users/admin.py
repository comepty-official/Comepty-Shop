from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'is_deleted', 'deleted_at']
    list_filter = ['is_deleted']
    search_fields = ['user__username', 'user__email']
    actions = ['restore_accounts']

    def restore_accounts(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)
        self.message_user(request, f'{queryset.count()} account(s) restored.')
    restore_accounts.short_description = 'Restore selected accounts'
