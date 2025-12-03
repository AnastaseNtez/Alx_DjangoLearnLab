from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Post, Comment
from .forms import UserRegisterForm, UserProfileUpdateForm, PostForm, CommentForm
from taggit.models import Tag # NEW: Import Tag model for filtering


# --- 1. USER AUTHENTICATION & PROFILE VIEWS ---

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Success message omitted; just redirect to login
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form, 'title': 'Register'})

@login_required
def profile(request):
    """Allows logged-in user to update their profile information."""
    if request.method == 'POST':
        u_form = UserProfileUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            # Success message omitted
            return redirect('profile')

    else:
        u_form = UserProfileUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        'title': 'Profile'
    }

    return render(request, 'blog/profile.html', context)


# --- 2. POST VIEWS (CRUD) ---

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    tag = None # Initialize tag attribute

    def get_queryset(self):
        # Start with the default queryset
        queryset = super().get_queryset()
        
        # Check if a tag_slug is provided in the URL (from the kwargs of the view)
        tag_slug = self.kwargs.get('tag_slug')

        if tag_slug:
            # Get the Tag object, or return 404 if not found
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            
            # Filter posts that are tagged with the specific tag
            # The '__in' lookup works because tags__in expects a list of IDs or objects, and [self.tag] provides that.
            queryset = queryset.filter(tags__in=[self.tag])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the current tag object to the context, if filtering, for display in the template
        if self.tag:
            context['tag'] = self.tag
        return context


class PostDetailView(DetailView):
    """Displays a single blog post and its comments."""
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    """Allows logged-in users to create a new post."""
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        # Set the author of the post to the current logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows post authors to update their existing posts."""
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows post authors to delete their existing posts."""
    model = Post
    success_url = reverse_lazy('blog:blog-home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# --- 3. COMMENT VIEWS (CRUD) ---

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    CBV to handle creating a new comment on a specific post.
    The parent Post PK is derived from the URL kwargs.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html' # Assuming you have a form template

    def get_post(self):
        """Helper to get the parent post object."""
        # 'pk' here refers to the Post's primary key from the URL (e.g., in /post/5/comment/new/)
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        # 1. Assign the current user as the author
        form.instance.author = self.request.user
        # 2. Assign the parent post
        form.instance.post = self.get_post()
        
        # 3. Save and continue
        return super().form_valid(form)

    def get_success_url(self):
        """Redirects to the parent post after successful creation."""
        # Redirect back to the post detail page
        return reverse('blog:post-detail', kwargs={'pk': self.kwargs.get('pk')})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows comment authors to update their comments."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        comment = self.get_object()
        return reverse('blog:post-detail', kwargs={'pk': comment.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows comment authors to delete their comments."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        comment = self.get_object()
        return reverse('blog:post-detail', kwargs={'pk': comment.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author