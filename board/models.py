from django.db import models
from django.conf import settings

class BoardPost(models.Model):
    POST_TYPE_CHOICES = [
        ('notice', '공지사항'),
        ('community', '커뮤니티'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    event_location = models.CharField(max_length=100, blank=True, null=True)
    event_start = models.DateTimeField(blank=True, null=True)
    event_end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_post_type_display()}] {self.title}"


class Comment(models.Model):
    post = models.ForeignKey('BoardPost', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')


    def __str__(self):
        return f"{self.author.name}의 댓글: {self.content[:20]}"
    
    @property
    def is_reply(self):
        return self.parent is not None