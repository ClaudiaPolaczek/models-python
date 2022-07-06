from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework import serializers
from .models import *
from users.serializers import RegisterSerializer, CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class UserReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'role', 'main_photo_url', 'avg_rate')


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
    image = serializers.ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = Image
        fields = ('id', 'portfolio', 'file_url', 'name', 'added_date')


class ImageWriterSerializer(serializers.ModelSerializer):
    file_url = Base64ImageField(
        max_length=None, use_url=True,
    )

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


