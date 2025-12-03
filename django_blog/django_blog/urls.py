from django.contrib import admin
from django.urls import path, include
# Import Django's built-in authentication views and alias them for clarity
from django.contrib.auth import views as auth_views 

urlpatterns = [
    # 1. Admin site URL
    path('admin/', admin.site.urls),
    
    # 2. Built-in Django Authentication Views (using class-based views)
    # The templates must exist in the 'blog' app's templates folder.
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    
    # 3. Delegate all root-level paths to the 'blog' app's urls.py file.
    # This is the last entry to catch everything else.
    path('', include('blog.urls')), 
]