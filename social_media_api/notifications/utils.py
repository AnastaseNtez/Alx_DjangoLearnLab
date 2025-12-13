# notifications/utils.py
from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(actor, recipient, verb, target):
    """Creates a notification instance."""
    if actor == recipient:
        return # Do not notify user for their own actions
        
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target=target
    )