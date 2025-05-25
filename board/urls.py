from django.urls import path
from .views import (
    NoticePostListView,
    CommunityPostListView,
    NoticePostCreateView,
    CommunityPostCreateView,
    NoticePostDetailView,
    CommunityPostDetailView,
)

urlpatterns = [
    path('notice/', NoticePostListView.as_view(), name='noticepost-list'),
    path('community/', CommunityPostListView.as_view(), name='communitypost-list'),
    
    path('notice/create/', NoticePostCreateView.as_view(), name='noticepost-create'),
    path('community/create/', CommunityPostCreateView.as_view(), name='communitypost-create'),
    
    path('notice/<int:pk>/', NoticePostDetailView.as_view(), name='noticepost-detail'),
    path('community/<int:pk>/', CommunityPostDetailView.as_view(), name='communitypost-detail'),
]

