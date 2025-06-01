from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import BoardPost, Comment
from .serializers import BoardPostSerializer, CommentSerializer

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

        post = serializer.save(author=self.request.user, post_type='notice')

         if post.event_start and post.event_end and post.event_location:
            CalendarEvent.objects.create(
                post=post,
                title=post.title,
                location=post.event_location,
                start=post.event_start,
                end=post.event_end
            )



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


class CommunityPostDetailView(generics.RetrieveDestroyAPIView):
    queryset = BoardPost.objects.filter(post_type='community')
    serializer_class = BoardPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("본인의 글만 삭제할 수 있습니다.")
        instance.delete()


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        try:
            post = BoardPost.objects.get(id=post_id)
        except BoardPost.DoesNotExist:
            raise NotFound("게시글이 존재하지 않습니다.")

        if post.post_type != 'community':
            raise PermissionDenied("공지사항에는 댓글을 작성할 수 없습니다.")

        serializer.save(author=self.request.user, post=post)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("본인의 댓글만 삭제할 수 있습니다.")
        instance.delete()