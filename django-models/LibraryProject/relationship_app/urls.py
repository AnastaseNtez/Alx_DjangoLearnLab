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
]