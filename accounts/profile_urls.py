from django.urls import path
from .views import UserProfileView, ProfileImageView, BuddyProfileEditView

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('me/profile-image/', ProfileImageView.as_view(), name='profile-image'),
    path('me/buddy-profile/', BuddyProfileEditView.as_view(), name='buddy-profile'),
]
