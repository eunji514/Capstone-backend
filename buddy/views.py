from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from datetime import timedelta
from django.utils import timezone
from django.db import models
from accounts.models import User, BuddyProfile
from .models import BuddyRelation   
from .serializers import BuddyRelationSerializer
from .utils import calculate_match_score, get_buddy_status_color
import random
from .permissions import IsBuddyEnabled

class BuddyRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBuddyEnabled]

    def post(self, request):
        target_id = request.data.get('buddy_id')
        if not target_id:
            return Response({'error': 'buddy_id is required'}, status=400)

        if str(request.user.id) == str(target_id):
            return Response({'error': '자기 자신에게는 요청할 수 없습니다.'}, status=400)

        try:
            buddy_user = User.objects.get(id=target_id)
        except User.DoesNotExist:
            return Response({'error': '대상 유저가 존재하지 않습니다.'}, status=404)

        # 이미 신청했는지 확인
        if BuddyRelation.objects.filter(user=request.user, buddy=buddy_user, status='requested').exists():
            return Response({'error': '이미 신청한 버디입니다.'}, status=409)

        # 내가 추가한 버디가 4명 넘는지 확인
        count = BuddyRelation.objects.filter(user=request.user, status='requested').count()
        if count >= 4:
            return Response({'error': '최대 4명까지 신청할 수 있습니다.'}, status=403)

        # 신청 생성
        relation = BuddyRelation.objects.create(
            user=request.user,
            buddy=buddy_user,
            status='requested'
        )

        return Response(BuddyRelationSerializer(relation).data, status=201)


class SentBuddyRequestsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsBuddyEnabled]
    serializer_class = BuddyRelationSerializer

    def get_queryset(self):
        return self.request.user.sent_requests.filter(status='requested')


class ReceivedBuddyRequestsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsBuddyEnabled]
    serializer_class = BuddyRelationSerializer

    def get_queryset(self):
        return self.request.user.received_requests.filter(status='requested')


class BuddyCancelRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBuddyEnabled]

    def delete(self, request):
        relation_id = request.data.get('relation_id')
        if not relation_id:
            return Response({'error': 'relation_id is required'}, status=400)

        try:
            relation = BuddyRelation.objects.get(
                id=relation_id,
                user=request.user,
                status='requested'
            )
        except BuddyRelation.DoesNotExist:
            return Response({'error': '취소할 요청이 존재하지 않거나 권한이 없습니다.'}, status=404)

        relation.status = 'cancelled'
        relation.save()

        return Response({'message': '신청이 취소되었습니다.'}, status=200)


class RespondBuddyRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBuddyEnabled]

    def patch(self, request):
        relation_id = request.data.get('relation_id')
        action = request.data.get('action')  # 'accept' 또는 'reject'

        if action not in ['accept', 'reject']:
            return Response({'error': 'action은 accept 또는 reject만 가능합니다.'}, status=400)

        try:
            relation = BuddyRelation.objects.get(id=relation_id, buddy=request.user)
        except BuddyRelation.DoesNotExist:
            return Response({'error': '해당 요청이 존재하지 않거나 권한이 없습니다.'}, status=404)

        if action == 'accept':
            # 이달의 나의 버디가 2명 이상이면 제한
            active_buddies = BuddyRelation.objects.filter(
                models.Q(user=request.user) | models.Q(buddy=request.user),
                status='accepted',
                accepted_at__gte=timezone.now() - timedelta(days=14)
            ).count()

            if active_buddies >= 2:
                return Response({'error': '이달의 나의 버디는 최대 2명까지 수락할 수 있습니다.'}, status=403)

            relation.status = 'accepted'
            relation.accepted_at = timezone.now()
            relation.save()
            return Response({'message': '수락 완료'}, status=200)

        elif action == 'reject':
            relation.status = 'rejected'
            relation.save()
            return Response({'message': '거절 완료'}, status=200)


class ActiveBuddyListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsBuddyEnabled]
    serializer_class = BuddyRelationSerializer

    def get_queryset(self):
        two_weeks_ago = timezone.now() - timedelta(days=14)
        return BuddyRelation.objects.filter(
            models.Q(user=self.request.user) | models.Q(buddy=self.request.user),
            status='accepted',
            accepted_at__gte=two_weeks_ago
        )


class RecommendBuddyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBuddyEnabled]

    def get(self, request):
        user = request.user
        try:
            my_profile = user.buddy_profile
        except BuddyProfile.DoesNotExist:
            return Response({'error': '버디 프로필이 존재하지 않습니다.'}, status=404)

        # 제외할 유저 목록: 나 자신, 이미 신청/수락한 상대
        sent_ids = user.sent_requests.values_list('buddy_id', flat=True)
        accepted_ids = BuddyRelation.objects.filter(
            models.Q(user=user) | models.Q(buddy=user),
            status='accepted'
        ).values_list('user_id', 'buddy_id')

        flat_accepted_ids = set()
        for u, b in accepted_ids:
            flat_accepted_ids.update([u, b])

        exclude_ids = set(sent_ids) | flat_accepted_ids | {user.id}

        # 추천 대상 필터링: 기능 on 사용자만 추천
        candidates = User.objects.filter(
            is_buddy_enabled=True,
            student_type='International' if user.student_type == 'Korean' else 'Korean'
        ).exclude(id__in=exclude_ids)

        # 점수 계산
        scored = [
            (c.buddy_profile, calculate_match_score(my_profile, c.buddy_profile))
            for c in candidates.select_related('buddy_profile')
            if hasattr(c, 'buddy_profile')
        ]

        scored.sort(key=lambda x: (-x[1], random.random()))  # 점수 내림차순 + 랜덤 요소

        top_4 = scored[:4]

        result = []
        for profile, score in top_4:
            result.append({
                'id': profile.user.id,
                'name': profile.user.name,
                'email': profile.user.email,
                'major': profile.user.major,
                'score': score,
                'interests': profile.interest.split(','),
                'languages': profile.language.split(','),
                'purposes': profile.purpose.split(','),
            })

        return Response(result)


class BuddyStatusColorView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        color = get_buddy_status_color(request.user)
        return Response({'status_color': color})


class BuddyMatchingStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'enabled': request.user.is_buddy_enabled})


class SetBuddyMatchingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        enabled = request.data.get('enabled')
        if not isinstance(enabled, bool):
            return Response({'error': 'enabled는 true 또는 false여야 합니다.'}, status=400)

        request.user.is_buddy_enabled = enabled
        request.user.save()
        return Response({'enabled': enabled})
