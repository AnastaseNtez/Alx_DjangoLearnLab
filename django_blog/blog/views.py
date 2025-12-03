from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import Post, Comment
from .forms import UserRegisterForm, PostForm, CommentForm 
from django.db.models import Q 

# --- Authentication and Profile Views ---

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form, 'title': 'Register'})

@login_required
def profile(request):
    context = {
        'title': 'Profile'
    }
    return render(request, 'blog/profile.html', context)

# --- Post CRUD Views ---

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts'
    ordering = ['-published_date'] 
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            queryset = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) | 
                Q(tags__name__icontains=query)
            ).distinct().order_by(self.ordering[0])
            
            return queryset

        return super().get_queryset() 

class PostByTagListView(PostListView):
    """Lists posts that have a specific tag, identified by the slug in the URL."""
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog-home') 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# --- Comment CRUD Views ---

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form.instance.post = post
        form.instance.author = self.request.user
        
        response = super().form_valid(form)
        
        # Redirect back to the post detail page
        return redirect('blog:post-detail', pk=post.pk)
    
    def get_success_url(self):
        # This is strictly used for CreateView, which is redirected manually above.
        return reverse('blog:post-detail', kwargs={'pk': self.kwargs.get('pk')})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows comment author to edit their comment."""
    model = Comment
    # Use fields instead of a form class for simple updates
    fields = ['content'] 
    template_name = 'blog/comment_form.html' # Reuse or create this template

    def get_success_url(self):
        # Redirect back to the post detail page the comment belongs to
        return reverse('blog:post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # Check if the logged-in user is the comment author
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows comment author to delete their comment."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html' # Must create this template

    def get_success_url(self):
        # Redirect back to the post detail page after successful deletion
        # Use self.object.post.pk to get the related post's primary key
        post_pk = self.object.post.pk
        return reverse_lazy('blog:post-detail', kwargs={'pk': post_pk})

    def test_func(self):
        # Check if the logged-in user is the comment author
        comment = self.get_object()
        return self.request.user == comment.author