from django.urls import path
from .views import (
    NoticePostListView,
    CommunityPostListView,
    NoticePostCreateView,
    CommunityPostCreateView,
    NoticePostDetailView,
    CommunityPostDetailView,
    CommentListCreateView,
    CommentDeleteView,
)

urlpatterns = [
    path('notice/', NoticePostListView.as_view(), name='noticepost-list'),
    path('community/', CommunityPostListView.as_view(), name='communitypost-list'),
    
    path('notice/create/', NoticePostCreateView.as_view(), name='noticepost-create'),
    path('community/create/', CommunityPostCreateView.as_view(), name='communitypost-create'),
    
    path('notice/<int:pk>/', NoticePostDetailView.as_view(), name='noticepost-detail'),
    path('community/<int:pk>/', CommunityPostDetailView.as_view(), name='communitypost-detail'),

    path('community/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]

