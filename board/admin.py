from django.contrib import admin
from .models import BoardPost, BoardPostImage

class BoardPostImageInline(admin.TabularInline):
    model = BoardPostImage
    extra = 1
    fields = ['board_image']

@admin.register(BoardPost)
class BoardPostAdmin(admin.ModelAdmin):
    inlines = [BoardPostImageInline]
    list_display = ['title','content', 'created_at', 'updated_at']
