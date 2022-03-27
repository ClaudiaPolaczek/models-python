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
    user = UserWriterSerializer(many=False)

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
    rating_user = UserWriterSerializer(many=False)
    rated_user = UserWriterSerializer(many=False)

    class Meta:
        model = Comment
        fields = ('rating_user', 'rated_user', 'rating', 'content')


class PortfolioReaderSerializer(serializers.ModelSerializer):
    user = UserReaderSerializer(many=False, read_only=True)

    class Meta:
        model = Portfolio
        fields = ('id', 'user', 'description', 'main_photo_url', 'added_date')


class PortfolioWriterSerializer(serializers.ModelSerializer):
    user = UserWriterSerializer(many=False)

    class Meta:
        model = Portfolio
        fields = ('user', 'description', 'main_photo_url')


class ImageReaderSerializer(serializers.ModelSerializer):
    portfolio = PortfolioReaderSerializer(many=False, read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'portfolio', 'file_url', 'name', 'added_date')


class ImageWriterSerializer(serializers.ModelSerializer):
    portfolio = PortfolioWriterSerializer(many=False)

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
    invited_user = UserWriterSerializer(many=False)
    inviting_user = UserWriterSerializer(many=False)

    class Meta:
        model = Photoshoot
        fields = ('invited_user', 'inviting_user', 'photoshoot_status', 'topic', 'notes', 'meeting_date', 'duration',
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


class PhotographerReaderSerializer(serializers.ModelSerializer):
    user = UserReaderSerializer(many=False, read_only=True)
    survey = SurveyReaderSerializer(many=False, read_only=True)

    class Meta:
        model = Photographer
        fields = ('id', 'user', 'survey')


class PhotographerWriterSerializer(serializers.ModelSerializer):
    #username = models.CharField(max_length=48)
    #user = RegisterSerializer(many=False)
    #survey = models.IntegerField()
    #survey = SurveyWriterSerializer(many=False)

    class Meta:
        model = Photographer
        fields = ('user', 'survey')

    def create(self, validated_data):
        user = validated_data.get('user')
        survey = validated_data.get('survey')
        #survey = Survey.objects.get(id=validated_data.get('survey'))
        user.role = User.PHOTOGRAPHER
        user.save()
        photographer = Photographer.objects.create(
                user=user,
                survey=survey)
        return photographer

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance

class AdditionalPhotographerWriterSerializer(serializers.Serializer):
    username = models.CharField(max_length=48, primary_key=True, unique=True)
    password = models.CharField(max_length=48)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birthday_year = models.IntegerField()
    gender = models.CharField(max_length=1)
    region = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=16)
    regulations_agreement = models.IntegerField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance


class ModelReaderSerializer(serializers.ModelSerializer):
    user = UserReaderSerializer(many=False, read_only=True)
    survey = SurveyReaderSerializer(many=False, read_only=True)

    class Meta:
        model = Model
        fields = ('id', 'user', 'eyes_color', 'hair_color', 'survey')


class ModelWriterSerializer(serializers.ModelSerializer):
    user = UserWriterSerializer(many=False)
    survey = SurveyWriterSerializer(many=False)

    def create(self, validated_data):
        user_serializer = UserWriterSerializer(validated_data.get('user'))
        user = user_serializer.save()
        user.role = user.PHOTOGRAPHER
        user.save()
        survey_serializer = SurveyWriterSerializer(validated_data.get('survey'))
        survey_serializer.save()
        return Model.objects.create(**validated_data)

    def update(self, validated_data):
        #TODO
        return Model.objects.create(**validated_data)

    class Meta:
        model = Model
        fields = ('user', 'eyes_color', 'hair_color', 'survey')
