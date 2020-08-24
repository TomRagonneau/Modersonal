from django.contrib import admin

from .forms import BlogCreationForm, BlogChangeForm, CommentCreationForm, CommentChangeForm
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    """Administration for blog posts."""

    add_form = BlogCreationForm
    form = BlogChangeForm

    list_display = ('title', 'author', 'visibility', 'status', 'created_on',)
    list_filter = ('visibility', 'status',)
    search_fields = ('title', 'content', 'slug',)
    ordering = ('created_on',)
    filter_horizontal = ()
    readonly_fields = ('slug', 'author', 'created_on', 'updated_on')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # The author should be added only at the first saving.
            obj.author = request.user
        super(PostAdmin, self).save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    """Administration for blog comments."""

    add_form = CommentCreationForm
    form = CommentChangeForm

    list_display = ('post', 'author', 'status', 'created_on',)
    list_filter = ('status',)
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('post', 'content', 'status')}),
    )
    fieldsets = (
        (None, {'fields': ('post', 'content', 'status')}),
    )
    search_fields = ('post', 'content',)
    ordering = ('created_on',)
    filter_horizontal = ()
    readonly_fields = ('author', 'created_on', 'updated_on')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # The author should be added only at the first saving.
            obj.author = request.user
        super(CommentAdmin, self).save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
