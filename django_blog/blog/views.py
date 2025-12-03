from django.shortcuts import render, redirect
# New: Required for successful redirects after CBV operations
from django.urls import reverse_lazy 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# New: Required for access control (security) on CBVs
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 

# New: Imports for all five Class-Based Views
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)

# New: Import the Post model and the required PostForm
from .models import Post 
# Ensure you import both the user form and the new Post form
from .forms import CustomUserCreationForm, PostForm 

# --- EXISTING AUTHENTICATION VIEWS (Kept from your original file) ---

# NOTE: The simple placeholder 'home_page' is removed. 
# The PostListView class below will now handle the main blog feed ('blog-home').

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


# --- NEW CRUD Views for Post Management ---

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
    """
    model = Post
    template_name = 'blog/post_detail.html' 
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allows authenticated users to create a new post (Create).
    Uses LoginRequiredMixin to ensure only logged-in users can access.
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
    Uses UserPassesTestMixin to ensure only the original author can update.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # We ensure the author remains the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Check if the current user is the author of the post they are trying to update.
        post = self.get_object() 
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows the post author to delete their post (Delete).
    Uses UserPassesTestMixin to ensure only the original author can delete.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html' 
    # Redirect back to the blog home list after successful deletion
    success_url = reverse_lazy('blog:blog-home') 

    def test_func(self):
        # Check if the current user is the author of the post they are trying to delete.
        post = self.get_object() 
        return self.request.user == post.author