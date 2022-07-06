from django.db import models
from django.utils import timezone
from django.conf import settings

from users.models import CustomUser as User


class Survey(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birthday_year = models.IntegerField()
    gender = models.CharField(max_length=1)
    region = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=16)
    instagram_name = models.CharField(max_length=32)
    regulations_agreement = models.IntegerField()


class Model(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    eyes_color = models.CharField(max_length=64)
    hair_color = models.CharField(max_length=64)
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.eyes_color = "-"
            self.hair_color = "-"
        return super(Model, self).save(*args, **kwargs)


class Photographer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE)


class Notification(models.Model):
    added_date = models.DateTimeField()
    content = models.TextField(max_length=500)
    read_value = models.IntegerField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #user = models.Many(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.added_date = timezone.now()
            self.read_value = 0
        return super(Notification, self).save(*args, **kwargs)


class Comment(models.Model):
    rating_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rating', on_delete=models.CASCADE)
    rated_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rated', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0.0)
    added_date = models.DateTimeField()
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.added_date = timezone.now()
        return super(Comment, self).save(*args, **kwargs)


class Photoshoot(models.Model):
    invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='invited_user', on_delete=models.SET_NULL, null=True)
    inviting_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='inviting_user', on_delete=models.SET_NULL, null=True)
    CREATED = 'C'
    ACCEPTED = 'A'
    CANCELED = 'D'
    ENDED = 'E'
    STATUS = [
        (CREATED, 'Created'),
        (ACCEPTED, 'Accepted'),
        (CANCELED, 'Canceled'),
        (ENDED, 'Ended'),
    ]
    photoshoot_status = models.CharField(max_length=1, choices=STATUS, default=CREATED)
    topic = models.CharField(max_length=64)
    notes = models.TextField()
    meeting_date = models.DateTimeField()
    duration = models.DurationField()
    city = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    house_number = models.CharField(max_length=64)


class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    description = models.TextField()
    main_photo_url = models.URLField(null=True)
    added_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.added_date = timezone.now()
        return super(Portfolio, self).save(*args, **kwargs)


class Image(models.Model):
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE)
    file_url = models.ImageField(upload_to="images")
    name = models.CharField(max_length=32)
    added_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.added_date = timezone.now()
        return super(Image, self).save(*args, **kwargs)
