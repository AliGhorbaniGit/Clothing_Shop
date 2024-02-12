from django.urls import path
from .views import product_detail_view, search_product_view, all_product_view, \
    CommentEdit, comment_reply_view, admin_awareness_check

app_name = 'shop'

urlpatterns = [
    path('', all_product_view, name='product_list'),
    path('<int:pk>/', product_detail_view, name='product_detail'),
    path('search/', search_product_view, name='search_product_view'),

    # path('order products/<int:pk>/', order_products_view, name='order_products'),
    path('comment update/<int:pk>/', CommentEdit.as_view(), name='edit_comment'),
    path('commentreply/', comment_reply_view, name='comment_reply'),
    path('admin_awareness_check/', admin_awareness_check, name='admin_awareness_check'),
]
