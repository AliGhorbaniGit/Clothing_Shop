from django.urls import path
from .views import ShowPackages, package_detail_view, package_search_view, profile_view, order_products_view, \
    CommentUpdate, comment_reply_view

urlpatterns = [
    path('', ShowPackages.as_view(), name='ShowPackages'),
    path('<int:pk>', package_detail_view, name='package_detail_view'),
    path('search/', package_search_view, name='package_search_view'),
    path('search/', package_search_view, name='package_search_view'),
    path('profile/', profile_view, name='profile'),
    path('order products/<int:pk>', order_products_view, name='order_products'),
    path('comment update/<int:pk>', CommentUpdate.as_view(), name='CommentUpdate'),
    path('commentreply/', comment_reply_view, name='CommentReply'),

    # path('<str:poll>', package_search_view, name='package_search_view'),
]
