from django.contrib import admin
from .models import User, BuddyProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'major', 'student_type')  
    list_filter = ('is_student_council', 'major', 'student_type')  
    search_fields = ('email', 'name')  

@admin.register(BuddyProfile)
class BuddyProfileAdmin(admin.ModelAdmin):
    list_display  = ('user_email', 'student_name')
    search_fields = ('user__email', 'user__name')

    def user_email(self, obj):
        return obj.user.email

    def student_name(self, obj):
        return obj.user.name
