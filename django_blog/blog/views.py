from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages # Required for the register function
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect 

# Import generic Class-Based Views
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# Import all necessary models and forms
from .models import Post, Comment 
from .forms import PostForm, CommentForm, CustomUserCreationForm 

# --- AUTHENTICATION VIEWS ---

def register(request):
    """
    Handles user registration using the CustomUserCreationForm.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form, 'title': 'Register'}
    return render(request, 'blog/register.html', context)

@login_required 
def profile(request):
    """
    Allows authenticated users to view their profile. 
    """
    context = {'title': 'Profile'}
    return render(request, 'blog/profile.html', context)


# --- POST CRUD VIEWS ---

class PostListView(ListView):
    """
    Displays a list of all blog posts (Read All). This serves as the main blog feed.
    """
    model = Post
    template_name = 'blog/post_list.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted'] # Order newest post first
    paginate_by = 10 

class PostDetailView(DetailView):
    """
    Displays a single blog post in full detail (Read One).
    Modified to also pass the CommentForm to the template.
    """
    model = Post
    template_name = 'blog/post_detail.html' 
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """Adds the CommentForm instance to the context."""
        context = super().get_context_data(**kwargs)
        # Pass an instance of the CommentForm to the template
        context['comment_form'] = CommentForm() 
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allows authenticated users to create a new post (Create).
    """
    model = Post
    form_class = PostForm 
    template_name = 'blog/post_form.html' 

    def form_valid(self, form):
        # Automatically set the author to the currently logged-in user before saving
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows the post author to update their post (Update).
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Check if the current user is the author of the post.
        post = self.get_object() 
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows the post author to delete their post (Delete).
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html' 
    success_url = reverse_lazy('blog:blog-home') 

    def test_func(self):
        # Check if the current user is the author of the post.
        post = self.get_object() 
        return self.request.user == post.author

# --- COMMENT CRUD VIEWS ---

@login_required
def add_comment(request, pk):
    """
    Function-Based View to handle the creation of a new comment (Create).
    It redirects back to the post detail page upon success or failure.
    """
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create, but do not save to the database yet
            comment = form.save(commit=False)
            
            # Set the required foreign keys
            comment.post = post
            comment.author = request.user
            
            # Save the comment
            comment.save()
            
            # Redirect back to the post detail page
            return HttpResponseRedirect(post.get_absolute_url())
    
    # If not a POST request or form is invalid, redirect back
    return HttpResponseRedirect(post.get_absolute_url())


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Class-Based View to handle editing an existing comment (Update).
    Only the comment author can access this.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def test_func(self):
        """Ensures only the comment author can edit the comment."""
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Class-Based View to handle deleting an existing comment (Delete).
    Only the comment author can access this.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def get_success_url(self):
        """Redirects to the parent post detail page after successful deletion."""
        comment = self.get_object()
        # Use reverse_lazy for the redirect URL
        return reverse_lazy('blog:post-detail', kwargs={'pk': comment.post.pk})

    def test_func(self):
        """Ensures only the comment author can delete the comment."""
        comment = self.get_object()
        return self.request.user == comment.author