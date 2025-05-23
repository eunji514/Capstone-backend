from django.urls import path
from .views import SignupUserInfoView, SignupBuddyInfoView

urlpatterns = [
    path('signup/userinfo/', SignupUserInfoView.as_view(), name='signup-userinfo'),
    path('signup/buddyinfo/', SignupBuddyInfoView.as_view(), name='signup-buddyinfo'),
]
