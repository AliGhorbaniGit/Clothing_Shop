from django.urls import path
from .views import ShowPackages, package_detail_view, package_search_view

urlpatterns = [
    path('', ShowPackages.as_view(), name='ShowPackages'),
    path('<int:pk>', package_detail_view, name='package_detail_view'),
    path('search/', package_search_view, name='package_search_view'),

    # path('<str:poll>', package_search_view, name='package_search_view'),
]
