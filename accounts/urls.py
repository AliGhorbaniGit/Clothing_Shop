from django.urls import path
from .views import profile_view, EditUserInformation, redirect_user

app_name = 'accounts'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('editt/<int:pk>/', EditUserInformation.as_view(), name='edit_user_information'),
    path('redirect/', redirect_user, name='redirect_user'),
]
