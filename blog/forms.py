from django import forms

from .models import Post, Comment


class BlogCreationForm(forms.ModelForm):
    """Creation form of blog posts."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BlogCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ('title', 'content', 'visibility', 'status',)


class CommentCreationForm(forms.ModelForm):
    """Creation form of blog comments."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CommentCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('content', 'status',)


class BlogChangeForm(forms.ModelForm):
    """Updating form of blog posts."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BlogChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ('title', 'content', 'visibility', 'status',)


class CommentChangeForm(forms.ModelForm):
    """Updating form of blog comments."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CommentChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('content', 'status',)
