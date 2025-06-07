from rest_framework import serializers
from .models import BuddyRelation
from accounts.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'major']


class BuddyRelationSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    buddy = UserSimpleSerializer(read_only=True)
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = BuddyRelation
        fields = [
            'id', 'user', 'buddy', 'status',
            'created_at', 'start_date', 'end_date', 'is_active'
        ]

    def get_start_date(self, obj):
        return obj.accepted_at.strftime("%Y-%m-%d") if obj.accepted_at else None

    def get_end_date(self, obj):
        end = obj.get_end_date()
        return end.strftime("%Y-%m-%d") if end else None

    def get_is_active(self, obj):
        return obj.is_active()
