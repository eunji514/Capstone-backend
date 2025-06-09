from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NoticePostListView,
    CommunityPostListView,
    NoticePostCreateView,
    CommunityPostCreateView,
    NoticePostDetailView,
    CommunityPostDetailView,
    CommentListCreateView,
    CommentDeleteView,
    translate_post,
    translate_comment,
    # PostViewSet,    
    BoardPostImageDeleteView,
)

# router = DefaultRouter()
# router.register('BoardPosts', PostViewSet)



urlpatterns = [
    path('notice/', NoticePostListView.as_view(), name='noticepost-list'),
    path('community/', CommunityPostListView.as_view(), name='communitypost-list'),
    
    path('notice/create/', NoticePostCreateView.as_view(), name='noticepost-create'),
    path('community/create/', CommunityPostCreateView.as_view(), name='communitypost-create'),
    
    path('notice/<int:pk>/', NoticePostDetailView.as_view(), name='noticepost-detail'),
    path('community/<int:pk>/', CommunityPostDetailView.as_view(), name='communitypost-detail'),

    path('community/<int:pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    path('<int:pk>/translate/', translate_post, name='translate-post'),
    path('comments/<int:pk>/translate/', translate_comment, name='translate-comment'),

    # path('', include(router.urls)),
    path('images/<int:pk>/delete/', BoardPostImageDeleteView.as_view(), name='board-image-delete'),
]

