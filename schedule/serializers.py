from rest_framework import serializers
from .models import CalendarEvent

class CalendarEventSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='post.id', read_only=True) 
    student_council_name = serializers.CharField(source='post.author.name', read_only=True)

    class Meta:
        model = CalendarEvent
        fields = ['id', 'title', 'location', 'start', 'end', 'post_id', 'student_council_name']
