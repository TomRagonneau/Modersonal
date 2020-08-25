from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.generic.edit import FormMixin

from .forms import BlogCreationForm, CommentCreationForm
from .models import Post, Comment, Like

BLOG_DIR = Path(__package__)


class PostListView(generic.ListView):
    """Post list view."""

    template_name = BLOG_DIR / 'home.html'
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(visibility=0)

        return queryset


class PostDetailView(FormMixin, generic.DetailView):
    """Post details view."""

    template_name = BLOG_DIR / 'details.html'
    model = Post
    form_class = CommentCreationForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            # A staff user has access to all the published and drafted comments.
            comment_query = Q()
        else:
            comment_query = Q(status=1)
            if self.request.user.is_authenticated:
                comment_query.add(Q(author=self.request.user), Q.OR)
        comment_query.add(Q(post_id=self.object), Q.AND)

        context.update({
            'comments': Comment.objects.filter(comment_query).order_by('created_on'),
        })
        if self.request.user.is_authenticated:
            context.update({'form': self.form_class()})

        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.object
        form.instance.author = self.request.user
        form.save()

        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name='dispatch')
class CreatePostView(generic.CreateView):
    """Post creation view."""

    template_name = BLOG_DIR / 'create.html'
    form_class = BlogCreationForm
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        # The author of the post is the authenticated user.
        form.instance.author = self.request.user
        return super(CreatePostView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class UpdatePostLike(View):
    """Update post like database."""

    redirect_to = reverse_lazy('blog:home')

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id', None)
        post = get_object_or_404(Post, id=post_id)
        referer = request.META.get('HTTP_REFERER', self.redirect_to)

        # Create the Like model relating to the post.
        try:
            post.likes
        except Like.DoesNotExist:
            Like.objects.create(post=post)

        # Dump/delete the like request into the database.
        if request.user in post.likes.users.all():
            post.likes.users.remove(request.user)
        else:
            post.likes.users.add(request.user)

        return HttpResponseRedirect(referer)

