from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import models, transaction
from django.db.models import Prefetch
from django.utils import timezone
from datetime import timedelta

from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from buddy.models import BuddyRelation
from accounts.models import User


class ChatRoomListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        user = self.request.user
        # 참여 중인 방 + 참가자, 마지막 메시지(prefetched) 동시 조회
        return ChatRoom.objects.filter(participants=user)\
            .prefetch_related(
                'participants',
                Prefetch(
                    'messages',
                    queryset=Message.objects.order_by('-timestamp')[:1],
                    to_attr='last_message_list'
                )
            )


class MessageListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        # 방에 속해있지 않으면 404
        room = get_object_or_404(
            ChatRoom.objects.prefetch_related('messages'),
            id=pk,
            participants=self.request.user
        )
        return room.messages.order_by('timestamp')

    def perform_create(self, serializer):
        room = get_object_or_404(
            ChatRoom,
            id=self.kwargs['pk'],
            participants=self.request.user
        )
        serializer.save(sender=self.request.user, room=room)


class ChatRoomGetOrCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        buddy_id = request.data.get('buddy_id')
        if not buddy_id:
            return Response({'error': 'buddy_id가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        buddy = get_object_or_404(User, id=buddy_id)

        # 반드시 수락된 버디 관계여야만 채팅방 생성 허용
        is_buddy = BuddyRelation.objects.filter(
            models.Q(user=request.user, buddy=buddy, status='accepted') |
            models.Q(user=buddy, buddy=request.user, status='accepted')
        ).exists()
        if not is_buddy:
            return Response({'error': '수락된 버디가 아닙니다.'}, status=status.HTTP_403_FORBIDDEN)

        # 트랜잭션으로 생성/조회 일관성 보장
        with transaction.atomic():
            room = ChatRoom.objects.filter(participants=request.user)\
                                   .filter(participants=buddy)\
                                   .first()
            if not room:
                room = ChatRoom.objects.create()
                room.participants.add(request.user, buddy)

        return Response({'room_id': room.id}, status=status.HTTP_200_OK)
