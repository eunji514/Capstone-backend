from rest_framework import serializers
from .models import ChatRoom, Message
from accounts.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']


class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSimpleSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'participants', 'last_message']

    def get_last_message(self, obj):
        last_msgs = getattr(obj, 'last_message_list', None)
        if last_msgs:
            return MessageSerializer(last_msgs[0]).data
        return None