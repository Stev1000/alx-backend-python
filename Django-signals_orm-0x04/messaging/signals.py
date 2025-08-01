from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification,MessageHistory
from django.db.models.signals import pre_save
from django.utils.timezone import now

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Only for existing messages
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                MessageHistory.objects.create(
                    message=original,
                    old_content=original.content,
                    edited_at=now()
                )
                instance.edited = True  # Mark as edited
        except Message.DoesNotExist:
            pass