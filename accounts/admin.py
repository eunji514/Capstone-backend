from django.contrib import admin
from .models import User, BuddyProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'major')  
    list_filter = ('is_student_council', 'major')  
    search_fields = ('email', 'name')  

@admin.register(BuddyProfile)
class BuddyProfileAdmin(admin.ModelAdmin):
    pass
