from django.urls import path
from .views import (
    BuddyRequestView,
    SentBuddyRequestsView,
    ReceivedBuddyRequestsView,
    RespondBuddyRequestView,
    ActiveBuddyListView,
    RecommendBuddyView,
    BuddyCancelRequestView,
    BuddyStatusColorView,
    BuddyMatchingStatusView,
    SetBuddyMatchingView,
)

urlpatterns = [
    path('request/', BuddyRequestView.as_view()),
    path('sent/', SentBuddyRequestsView.as_view()),
    path('received/', ReceivedBuddyRequestsView.as_view()),
    path('respond/', RespondBuddyRequestView.as_view()),
    path('active/', ActiveBuddyListView.as_view()),
    path('recommend/', RecommendBuddyView.as_view()),
    path('cancel/', BuddyCancelRequestView.as_view()),
    path('status-color/', BuddyStatusColorView.as_view()),
    path('matching-status/', BuddyMatchingStatusView.as_view()),
    path('set-matching/', SetBuddyMatchingView.as_view()),
]
