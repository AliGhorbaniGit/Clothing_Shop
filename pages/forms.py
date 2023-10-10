from django import forms

from .models import Comment, ReplyComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class CommentUdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = ReplyComment
        fields = ('text', 'reply_author', 'reply_package_name', 'comment_name',)
        # fields = ('text',)
