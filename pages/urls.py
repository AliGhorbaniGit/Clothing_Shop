from django.urls import path
from .views import ShowPackages


urlpatterns = [
    path('', ShowPackages.as_view(), name='ShowPackages'),
]
