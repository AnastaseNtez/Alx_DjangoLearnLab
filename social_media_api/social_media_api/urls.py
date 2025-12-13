# social_media_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Existing accounts app URLs
    path('api/accounts/', include('accounts.urls')),
    # NEW posts app URLs under /api/
    path('api/', include('posts.urls')), 
    path('api/notifications/', include('notifications.urls')),
]