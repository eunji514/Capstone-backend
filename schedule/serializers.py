from rest_framework import serializers
from .models import CalendarEvent

class CalendarEventSerializer(serializers.ModelSerializer):
    student_council_name = serializers.CharField(source='student_council.name')
    student_council_color = serializers.CharField(source='student_council.color')
    
    class Meta:
        model = CalendarEvent
        fields = ['id', 'title', 'location', 'start', 'end', 'student_council_name', 'student_council_color']
