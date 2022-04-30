from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework import serializers
from .models import *
from users.serializers import RegisterSerializer, CustomUserSerializer


class UserReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'role', 'main_photo_url', 'avg_rate')


class UserWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'role', 'main_photo_url')


class NotificationReaderSerializer(serializers.ModelSerializer):
    user = UserReaderSerializer(many=False, read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'added_date', 'content', 'read_value', 'user')


class NotificationWriterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('content', 'user')


class CommentReaderSerializer(serializers.ModelSerializer):
    rating_user = UserReaderSerializer(many=False, read_only=True)
    rated_user = UserReaderSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'rating_user', 'rated_user', 'rating', 'added_date', 'content')


class CommentWriterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('rating_user', 'rated_user', 'rating', 'content')


class PortfolioReaderSerializer(serializers.ModelSerializer):
    user = UserReaderSerializer(many=False, read_only=True)

    class Meta:
        model = Portfolio
        fields = ('id', 'user', 'name', 'description', 'main_photo_url', 'added_date')


class PortfolioWriterSerializer(serializers.ModelSerializer):
    main_photo_url = serializers.URLField(allow_blank=True)

    class Meta:
        model = Portfolio
        fields = ('user', 'name', 'description', 'main_photo_url')


class ImageReaderSerializer(serializers.ModelSerializer):
    portfolio = PortfolioReaderSerializer(many=False, read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'portfolio', 'file_url', 'name', 'added_date')


class ImageWriterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('portfolio', 'file_url', 'name')


class PhotoshootReaderSerializer(serializers.ModelSerializer):
    invited_user = UserReaderSerializer(many=False, read_only=True)
    inviting_user = UserReaderSerializer(many=False, read_only=True)

    class Meta:
        model = Photoshoot
        fields = ('id', 'invited_user', 'inviting_user', 'photoshoot_status', 'topic', 'notes', 'meeting_date',
                  'duration', 'city', 'street', 'house_number')


class PhotoshootWriterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photoshoot
        fields = ('invited_user', 'inviting_user', 'topic', 'notes', 'meeting_date', 'duration',
                  'city', 'street', 'house_number')


class SurveyReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'first_name', 'last_name', 'birthday_year', 'gender', 'region', 'city',
                  'phone_number', 'instagram_name', 'regulations_agreement')


class SurveyWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('first_name', 'last_name', 'birthday_year', 'gender', 'region', 'city',
                  'phone_number', 'regulations_agreement')


class PhotographerSerializer(serializers.ModelSerializer):
    user = UserReaderSerializer(many=False, read_only=True)
    survey = SurveyReaderSerializer(many=False, read_only=True)

    class Meta:
        model = Photographer
        fields = ('id', 'user', 'survey')
        depth = 1


class ModelSerializer(serializers.ModelSerializer):
    user = UserReaderSerializer(many=False, read_only=True)
    survey = SurveyReaderSerializer(many=False, read_only=True)

    class Meta:
        model = Model
        fields = ('id', 'user', 'eyes_color', 'hair_color', 'survey')
        depth = 1
