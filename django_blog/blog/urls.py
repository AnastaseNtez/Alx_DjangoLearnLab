from django.urls import path
from django.contrib.auth import views as auth_views # Import built-in auth views
from . import views # Import custom FBVs: home_page, register, profile
from .views import ( # Import Class-Based Views for Post CRUD
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

# Sets the namespace for this app, e.g., blog:blog-home
app_name = 'blog'

urlpatterns = [
    
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'), 
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

]

# 1Home page / Post List View (Class-Based View)
    #The 'blog-home' name is used throughout the project (e.g., in base.html)
    
    # 2. Post Detail View (CBV)
    
    
    # 3. Post Create View (CBV) - Requires 'post/new/' according to checker
    

    # 4. Post Update View (CBV)
    
    
    # 5. Post Delete View (CBV)
   
    
    #  Custom User Auth Views (Function-Based) ---
    # --- Built-in Django Authentication Views ---
    # These were previously included in your uploaded urls.py and are needed.