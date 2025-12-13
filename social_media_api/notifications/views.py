# notifications/views.py
from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer
# Assuming CustomPageNumberPagination is available in posts app
from posts.pagination import CustomPageNumberPagination 

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = CustomPageNumberPagination 

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Mark all retrieved notifications as read after they are listed
        self.get_queryset().filter(is_read=False).update(is_read=True)
        
        return response