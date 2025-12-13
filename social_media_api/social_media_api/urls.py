# social_media_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the accounts app URLs under the /api/accounts/ namespace
    path('api/accounts/', include('accounts.urls')),
]