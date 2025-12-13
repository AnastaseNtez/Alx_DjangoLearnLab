# notifications/serializers.py
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source='actor.username')
    target_type = serializers.ReadOnlyField(source='content_type.model')

    class Meta:
        model = Notification
        fields = (
            'id', 'actor', 'actor_username', 'verb', 'target_type', 'object_id', 
            'timestamp', 'is_read'
        )
        read_only_fields = fields