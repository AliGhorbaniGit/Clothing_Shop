from django.urls import path
from .views import ShowPackages, package_detail_view


urlpatterns = [
    path('', ShowPackages.as_view(), name='ShowPackages'),
    path('<int:pk>', package_detail_view, name='package_detail_view')
]
