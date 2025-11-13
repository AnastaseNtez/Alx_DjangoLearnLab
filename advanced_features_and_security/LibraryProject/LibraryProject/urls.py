from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Changed RedirectView to TemplateView
from django.views.generic import TemplateView 

urlpatterns = [
    # 1. Root URL (/) now renders the simple index.html homepage.
    # Standard users will land here after login, since LOGIN_REDIRECT_URL = '/'
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    path('admin/', admin.site.urls),
    
    # 2. Include the bookshelf app's URLs under the 'bookshelf/' path
    path('bookshelf/', include('LibraryProject.bookshelf.urls')),
    
    # 3. Include the default authentication URLs (e.g., login, logout, password change)
    path('accounts/', include('django.contrib.auth.urls')),
]

# Serve media files (like profile photos) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)