from django import forms

from .models import Comment, ReplyComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = ReplyComment
        fields = ('reply_author', 'reply_product', 'reply_comment', 'text',)


class SearchForm(forms.Form):
    text = forms.CharField(max_length=40, error_messages={'required': 'Please enter some alphabet characters'})
