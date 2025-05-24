from django.urls import path
from .views import SignupUserInfoView, SignupBuddyInfoView, EmailVerificationRequestView, EmailVerificationConfirmView

urlpatterns = [
    path('userinfo/', SignupUserInfoView.as_view(), name='signup-userinfo'),
    path('buddyinfo/', SignupBuddyInfoView.as_view(), name='signup-buddyinfo'),
    path('email-verify/', EmailVerificationRequestView.as_view(), name='email-verify'),
    path('email-verify/confirm/', EmailVerificationConfirmView.as_view(), name='email-verify-confirm'),
]
