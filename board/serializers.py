from rest_framework import serializers
from .models import BoardPost, Comment, BoardPostImage

class BoardPostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardPostImage
        fields = ['id', 'board_image']


class BoardPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    author_student_id = serializers.CharField(source='author.student_id', read_only=True)
    author_major = serializers.CharField(source='author.get_major_display', read_only=True)
    board_images = BoardPostImageSerializer(many=True, read_only=True)
    

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
            'event_location',
            'event_start',
            'event_end',
        ]
        read_only_fields = ['created_at', 'updated_at', 'author_name', 'author_student_id', 'author_major', 'translated_content', 'original_language']

    def create(self, validated_data):
        uploaded_images = self.context['request'].FILES.getlist('uploaded_images')
        post = BoardPost.objects.create(**validated_data)
        for image in uploaded_images:
            BoardPostImage.objects.create(post=post, board_image=image)
        return post

    # def create(self, validated_data):
    #     board_image_data = self.context['request'].FILES
    #     BoardPost = BoardPost.objects.create(**validated_data)
    #     for board_image_data in board_image_data.getlist('image'):
    #         BoardPostImage.objects.create(BoardPost = BoardPost, board_image = board_image_data)
    #     return BoardPost




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