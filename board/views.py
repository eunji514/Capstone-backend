from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import BoardPost
from .serializers import BoardPostSerializer

class NoticePostListView(generics.ListAPIView):
    serializer_class = BoardPostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return BoardPost.objects.filter(post_type='notice').order_by('-created_at')


class CommunityPostListView(generics.ListAPIView):
    serializer_class = BoardPostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return BoardPost.objects.filter(post_type='community').order_by('-created_at')


class NoticePostCreateView(generics.CreateAPIView):
    serializer_class = BoardPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("공지사항은 관리자만 작성할 수 있습니다.")
        serializer.save(author=self.request.user, post_type='notice')


class CommunityPostCreateView(generics.CreateAPIView):
    serializer_class = BoardPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_type='community')


class NoticePostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardPost.objects.filter(post_type='notice')
    serializer_class = BoardPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("공지사항은 관리자만 수정할 수 있습니다.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("공지사항은 관리자만 삭제할 수 있습니다.")
        instance.delete()


class CommunityPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardPost.objects.filter(post_type='community')
    serializer_class = BoardPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("본인의 글만 수정할 수 있습니다.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("본인의 글만 삭제할 수 있습니다.")
        instance.delete()
