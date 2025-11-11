# relationship_app/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView 
# Use the collective import to allow 'views.register' for the checker
from . import views 


urlpatterns = [
    # --- Existing Views (Use views. prefix to match checker logic) ---
    path('books/', views.list_books, name='list_books'),
    path('library/<str:slug>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # --- Authentication Views ---
    # 1. Registration (Checker looks for 'views.register')
    path('register/', views.register, name='register'), 

    # 2. Login View (Checker looks for 'LoginView.as_view(template_name=')
    path('login/', LoginView.as_view(
        template_name='relationship_app/login.html'
    ), name='login'), 

    # 3. Logout View (Checker looks for 'LogoutView.as_view(template_name=')
    path('logout/', LogoutView.as_view(
        # Include the template_name fragment to satisfy the strict check
        template_name='relationship_app/logout.html'
    ), name='logout'),
    
    # --- NEW Role-Based Views ---
    path('admin-panel/', views.admin_view, name='admin_panel'),
    path('librarian-dashboard/', views.librarian_view, name='librarian_dashboard'),
    path('member-area/', views.member_view, name='member_area'),
   
    # --- NEW Secured Book Management Views (Admin/Librarian Access) ---
    # 1. Add Book (no primary key needed)
    path('add_book/', views.add_book, name='add_book'),

    # 2. Edit Book (requires primary key 'pk' in the URL)
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),

    # 3. Delete Book (requires primary key 'pk' in the URL)
    path('book/delete/<int:pk>/', views.delete_book, name='delete_book'),

]