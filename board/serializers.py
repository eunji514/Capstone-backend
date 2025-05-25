from rest_framework import serializers
from .models import BoardPost

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
            'created_at',
            'updated_at',
            'author_name',
            'author_student_id',
            'author_major',
        ]
        read_only_fields = ['created_at', 'updated_at', 'author_name', 'author_student_id', 'author_major']
