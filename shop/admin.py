from django.contrib import admin

from .models import Product, Comment, ReplyComment, ProductColorSizeCount, AdminAwareness


class ProductColorSizeCountInline(admin.TabularInline):
    model = ProductColorSizeCount
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['author', 'text', 'is_confirmed', ]
    extra = 1


class ProductColorSizeCountAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'color_1', 'how_many_color_1', 'color_2', 'how_many_color_2', 'color_3',
                    'how_many_color_3', 'color_4', 'how_many_color_4', 'datetime_created', ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'product', 'text', 'date_created', 'is_confirmed', ]
    list_editable = ['is_confirmed', ]
    list_per_page = 20
    search_fields = ['is_confirmed', 'author', 'product' ]
    list_filter = ['date_created', 'is_confirmed', ]


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'material', 'is_offer', 'offer_percent', 'show', 'available', 'datetime_created']
    inlines = [ProductColorSizeCountInline, CommentInline, ]


class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ['reply_author', 'text']
    list_per_page = 20
    search_fields = ['reply_author', ]
    list_filter = ['reply_author',  ]


class AdminAwarenessAdmin(admin.ModelAdmin):
    list_display = ['sender', 'subject', 'access_way', 'is_checked']
    list_editable = ['is_checked', ]
    list_per_page = 20
    search_fields = ['sender', ]
    list_filter = ['sender', 'is_checked', ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ProductColorSizeCount, ProductColorSizeCountAdmin)
admin.site.register(ReplyComment, CommentReplyAdmin)
admin.site.register(AdminAwareness, AdminAwarenessAdmin)
