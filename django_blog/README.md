Django Blog Project: Blog Post Management (CRUD)

This project features comprehensive CRUD (Create, Read, Update, Delete) operations for managing blog posts, allowing authenticated users (authors) to control their content dynamically.

Key Features Implemented

1. Post Model

Model: Post (in blog/models.py)

Fields: title, content, date_posted, and author (linked to User model).

get_absolute_url: Ensures proper redirection to the post detail page after creation or update.

2. CRUD Views (Class-Based Views in blog/views.py)

View Class

Functionality

URL Name

Access Control

PostListView

Displays all posts (Home Page).

blog:blog-home

All Users

PostDetailView

Displays a single post.

blog:post-detail

All Users

PostCreateView

Handles post creation form submission.

blog:post-create

Login Required (LoginRequiredMixin)

PostUpdateView

Handles post editing form submission.

blog:post-update

Login Required (LoginRequiredMixin) & Author Only (UserPassesTestMixin)

PostDeleteView

Handles post deletion confirmation.

blog:post-delete

Login Required (LoginRequiredMixin) & Author Only (UserPassesTestMixin)

3. Permissions and Security

Login Required: Creating posts requires the user to be logged in.

Author Protection: Editing or deleting a post is strictly limited to the author who created it, enforced using UserPassesTestMixin in the UpdateView and DeleteView.

4. URL Patterns (blog/urls.py)

Path

Purpose

Example URL

path('', ...)

Main list of all posts.

/

path('post/new/', ...)

Form to create a new post.

/post/new/

path('post/<int:pk>/', ...)

View a specific post.

/post/123/

path('post/<int:pk>/update/', ...)

Form to edit a specific post.

/post/123/update/

path('post/<int:pk>/delete/', ...)

Confirmation page to delete a specific post.

/post/123/delete/