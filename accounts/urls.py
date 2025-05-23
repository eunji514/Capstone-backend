from django.urls import path
from .views import SignupUserInfoView, SignupBuddyInfoView

urlpatterns = [
    path('userinfo/', SignupUserInfoView.as_view(), name='signup-userinfo'),
    path('buddyinfo/', SignupBuddyInfoView.as_view(), name='signup-buddyinfo'),
]
