from rest_framework import serializers
from .models import BoardPost, Comment

class BoardPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    author_student_id = serializers.CharField(source='author.student_id', read_only=True)
    author_major = serializers.CharField(source='author.get_major_display', read_only=True)

    class Meta:
        model = BoardPost
        fields = [
            'id',
            'title',
            'content',
            'translated_content',
            'original_language',
            'created_at',
            'updated_at',
            'author_name',
            'author_student_id',
            'author_major',
            'board_images',
        ]
        read_only_fields = ['created_at', 'updated_at', 'author_name', 'author_student_id', 'author_major', 'translated_content', 'original_language']


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'author_name', 'created_at', 'parent', 'replies', 'translated_content', 'original_language']
        read_only_fields = ['id', 'author_name', 'created_at', 'replies', 'translated_content', 'original_language']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []