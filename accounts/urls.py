from django.urls import path
from .views import SignupUserInfoView

urlpatterns = [
    path('signup/userinfo/', SignupUserInfoView.as_view(), name='signup-userinfo'),
    path('signup/buddyinfo/', SignupBuddyInfoView.as_view(), name='signup-buddyinfo'),
]
