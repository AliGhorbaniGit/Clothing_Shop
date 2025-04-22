from django.contrib import admin

from .models import CustomUser
from shop.models import Comment, ReplyComment
from orders.models import Order
from contactus.models import ContactUs


class UserCommentInline(admin.TabularInline):
    model = Comment
    fields = ['text', 'product', 'is_confirmed']
    extra = 1


class UserOrdersInline(admin.TabularInline):
    model = Order
    fields = ['is_paid', 'first_name', 'last_name', 'phone_number', ]
    extra = 1


class UserContactusInline(admin.TabularInline):
    model = ContactUs
    fields = ['user_text', 'admin_text', 'is_new', ]
    extra = 1


class UserReplyCommentInline(admin.TabularInline):
    model = ReplyComment
    fields = ['reply_product', 'reply_comment', 'text', ]
    extra = 1


class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'number', 'image']
    inlines = [UserOrdersInline, UserCommentInline, UserContactusInline, UserReplyCommentInline]
    list_per_page = 20
    search_fields = ["id", 'product', ]
    list_filter = ['username', 'first_name', 'number', ]


admin.site.register(CustomUser, UsersAdmin)
