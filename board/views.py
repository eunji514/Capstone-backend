from openai import OpenAI
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from config import config
from langdetect import detect
from .models import BoardPost, Comment, BoardPostImage
from .serializers import BoardPostSerializer, CommentSerializer, BoardPostImageSerializer
from schedule.models import CalendarEvent

client = OpenAI(api_key=config.OPENAI_API_KEY)

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
        if not self.request.user.is_student_council:
            raise PermissionDenied("공지사항은 관리자만 작성할 수 있습니다.")

        post = serializer.save(author=self.request.user, post_type='notice')

        if post.event_start and post.event_end: # 시간 설정하면 캘린더 표시
            CalendarEvent.objects.create(
                post=post,
                title=post.title,
                location=post.event_location,
                start=post.event_start,
                end=post.event_end,
                # student_council=post.author.name
            )


class CommunityPostCreateView(generics.CreateAPIView):
    serializer_class = BoardPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_type='community')


# class PostViewSet(ModelViewSet):
#     queryset = BoardPost.objects.all()
#     serializer_class = BoardPostSerializer
#     permission_classes = [permissions.AllowAny]

#     # def perform_create(self, serializer):
#     #     serializer.save(author=self.request.user)
    

class NoticePostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardPost.objects.filter(post_type='notice')
    serializer_class = BoardPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if not self.request.user.is_student_council:
            raise PermissionDenied("공지사항은 관리자만 수정할 수 있습니다.")
        
        post = serializer.save()

        for img in self.request.FILES.getlist('uploaded_images'):
            BoardPostImage.objects.create(post=post, board_image=img)

        if post.event_start and post.event_end:
            CalendarEvent.objects.update_or_create(
                post=post,
                defaults={
                    'title':           post.title,
                    'location':        post.event_location,
                    'start':           post.event_start,
                    'end':             post.event_end,
                    # 'student_council': post.author.name,
                }
            )
        else:
            CalendarEvent.objects.filter(post=post).delete()

    def perform_destroy(self, instance):
        if not self.request.user.is_student_council:
            raise PermissionDenied("공지사항은 관리자만 삭제할 수 있습니다.")
        
        CalendarEvent.objects.filter(post=instance).delete()

        instance.delete()


class CommunityPostDetailView(generics.RetrieveDestroyAPIView):
    queryset = BoardPost.objects.filter(post_type='community')
    serializer_class = BoardPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("본인의 글만 삭제할 수 있습니다.")
        instance.delete()


class BoardPostImageDeleteView(generics.DestroyAPIView):
    queryset = BoardPostImage.objects.all()
    serializer_class = BoardPostImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        post = instance.post
        if post.post_type != 'notice':
            raise PermissionDenied("커뮤니티 글의 이미지는 삭제할 수 없습니다.")
        if not self.request.user.is_student_council:
            raise PermissionDenied("공지사항 이미지는 관리자만 삭제할 수 있습니다.")
        instance.delete()


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comment.objects.filter(post__id=pk, parent=None)

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        try:
            post = BoardPost.objects.get(id=pk)
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


def detect_language(text):
    try:
        return detect(text)
    except:
        return 'unknown'

def gpt_translate(text, target_lang):
    system_prompt = """
    You are a professional translator. Translate the following text to {target_lang}.
    Maintain the original meaning, tone, and format while providing natural translation.
    If there are any cultural-specific terms, provide appropriate equivalents in the target language.
    """.format(target_lang=target_lang)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content.strip()


@api_view(['POST'])
def translate_post(request, pk):
    try:
        post = BoardPost.objects.get(pk=pk)
    except BoardPost.DoesNotExist:
        raise NotFound("해당 게시글이 존재하지 않습니다.")

    user_lang = request.data.get('language', 'ko')
    content = post.content
    source_lang = detect_language(content)
    
    # 번역 방향 결정
    if source_lang == 'ko':
        target_lang = 'en'
    elif source_lang == 'en':
        target_lang = 'ko'
    else:
        target_lang = user_lang

    # GPT 번역 실행
    translated = gpt_translate(content, target_lang)

    # 저장
    post.original_language = source_lang
    post.translated_content = translated
    post.save()

    return Response({
        'original': content,
        'translated': translated,
        'original_language': source_lang,
        'target_language': target_lang,
    })


@api_view(['POST'])
def translate_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        raise NotFound("해당 댓글이 존재하지 않습니다.")

    user_lang = request.data.get('language', 'ko')
    content = comment.content
    source_lang = detect_language(content)

    if source_lang == 'ko':
        target_lang = 'en'
    elif source_lang == 'en':
        target_lang = 'ko'
    else:
        target_lang = user_lang

    translated = gpt_translate(content, target_lang)

    comment.original_language = source_lang
    comment.translated_content = translated
    comment.save()

    return Response({
        'original': content,
        'translated': translated,
        'original_language': source_lang,
        'target_language': target_lang,
    })
