from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from .fields import RandomSlugField

# Quick-start model field settings
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)
VISIBILITY = ((0, _('Everybody')), (1, _('Authenticated users only')))
STATUS = ((0, _('Draft')), (1, _('Published')))
POST_SLUG_MAX_LENGTH = getattr(settings, 'POST_SLUG_MAX_LENGTH', 15)
POST_TITLE_MAX_LENGTH = getattr(settings, 'POST_TITLE_MAX_LENGTH', 200)


class Post(models.Model):
    """Blog post model."""

    slug = RandomSlugField(length=POST_SLUG_MAX_LENGTH, unique=True)
    title = models.CharField(max_length=POST_TITLE_MAX_LENGTH)
    author = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    visibility = models.IntegerField(choices=VISIBILITY, default=0)
    status = models.IntegerField(choices=STATUS, default=0)

    def count_likes(self):
        try:
            return self.likes.users.count()
        except Like.DoesNotExist:
            return 0

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']


class Comment(models.Model):
    """Blog comment model."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.content[:200]

    class Meta:
        ordering = ['-created_on']


class Like(models.Model):
    """Blog like model."""

    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='likes')
    users = models.ManyToManyField(USER_MODEL, related_name='likes')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post)
