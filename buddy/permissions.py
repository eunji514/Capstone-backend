from rest_framework import permissions

class IsBuddyEnabled(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'is_buddy_enabled', False)
