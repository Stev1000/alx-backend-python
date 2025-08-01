from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class NotificationSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='pass123')
        self.receiver = User.objects.create_user(username='bob', password='pass123')

    def test_notification_created_when_message_sent(self):
        self.assertEqual(Notification.objects.count(), 0)
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hi Bob!')
        self.assertEqual(Notification.objects.count(), 1)
        notif = Notification.objects.first()
        self.assertEqual(notif.user, self.receiver)
        self.assertEqual(notif.message, message)
