from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import TblUser
from .fields import RandomSlugField

# Quick-start model field settings
VISIBILITY = ((0, _('Everybody')), (1, _('Authenticated users only')))
STATUS = ((0, _('Draft')), (1, _('Published')))
POST_SLUG_MAX_LENGTH = getattr(settings, 'POST_SLUG_MAX_LENGTH', 15)
POST_TITLE_MAX_LENGTH = getattr(settings, 'POST_TITLE_MAX_LENGTH', 200)


class Post(models.Model):
    """Blog post model."""

    slug = RandomSlugField(length=POST_SLUG_MAX_LENGTH, unique=True)
    title = models.CharField(max_length=POST_TITLE_MAX_LENGTH)
    author = models.ForeignKey(TblUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    visibility = models.IntegerField(choices=VISIBILITY, default=0)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']


class Comment(models.Model):
    """Blog comment model."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(TblUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']
