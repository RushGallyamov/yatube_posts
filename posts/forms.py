from .models import Post, Comment
from django import forms
from django.forms import ModelForm


class PostForm(ModelForm):
    """Форма создания поста"""
    text = forms.CharField(
        widget=forms.Textarea,
        max_length=700,
        label='Текст поста'
    )

    class Meta:
        model = Post
        fields = ['group', 'text', 'image']


class CommentForm(ModelForm):
    """Форма создания Комментария"""
    text = forms.CharField(
        widget=forms.Textarea,
        max_length=700,
        label='Текст комментария'
    )

    class Meta:
        model = Comment
        fields = ['text']
