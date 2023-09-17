from django.contrib import admin

from .models import Package, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['text', ]


class PackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    inlines = [CommentInline, ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'text']


admin.site.register(Package, PackageAdmin)
admin.site.register(Comment, CommentAdmin)
