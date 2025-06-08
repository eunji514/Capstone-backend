from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import EmailVerificationRequestView, EmailVerificationConfirmView, LogoutView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('email-verify/', EmailVerificationRequestView.as_view(), name='email-verify'),
    path('email-verify/confirm/', EmailVerificationConfirmView.as_view(), name='email-verify-confirm'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
