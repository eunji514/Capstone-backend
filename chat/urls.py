from django.urls import path
from .views import (
    ChatRoomListView,
    MessageListCreateView,
    ChatRoomGetOrCreateView,
)

urlpatterns = [
    path('', ChatRoomListView.as_view()),
    path('create/', ChatRoomGetOrCreateView.as_view()),
    path('<int:pk>/messages/', MessageListCreateView.as_view()),
]