from django.contrib import admin
from .models import BuddyRelation

@admin.register(BuddyRelation)
class BuddyRelationAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'buddy_name', 'status', 'created_at', 'accepted_at', 'is_active_buddy')
    list_filter = ('status', 'created_at', 'accepted_at')
    search_fields = ('user__name', 'buddy__name', 'user__email', 'buddy__email')
    date_hierarchy = 'created_at'

    def user_name(self, obj):
        return f"{obj.user.name} ({obj.user.email})"
    user_name.short_description = '요청자'

    def buddy_name(self, obj):
        return f"{obj.buddy.name} ({obj.buddy.email})"
    buddy_name.short_description = '수락자'
