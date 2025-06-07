from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class BuddyRelation(models.Model):
    class Status(models.TextChoices):
        REQUESTED = 'requested', '요청됨'      # 내가 보낸 요청
        PENDING = 'pending', '대기중'         # 나를 추가한 버디
        ACCEPTED = 'accepted', '수락됨'         # 매칭 수락
        REJECTED = 'rejected', '거절됨'         # 매칭 거절
        CANCELLED = 'cancelled', '취소됨'       # 신청 취소

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )
    buddy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_requests'
    )
    status = models.CharField(max_length=10, choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    def is_active_buddy(self):
        if self.status == 'accepted' and self.accepted_at:
            return timezone.now() <= self.accepted_at + timedelta(days=14)
        return False

    def get_end_date(self):
        if self.accepted_at:
            return self.accepted_at + timedelta(days=14)
        return None

    def __str__(self):
        return f"{self.user.name} → {self.buddy.name} [{self.status}]"
