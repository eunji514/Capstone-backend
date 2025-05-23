from django.urls import path
from .views import SignupUserInfoView

urlpatterns = [
    path('signup/userinfo/', SignupUserInfoView.as_view(), name='signup-userinfo'),
]
