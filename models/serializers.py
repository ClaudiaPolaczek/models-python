from rest_framework import serializers
from .models import Notification

class NotificationReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('notification_id', 'added_date', 'content', 'read_value', 'user_username')

class NotificationWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('content', 'user_username')

