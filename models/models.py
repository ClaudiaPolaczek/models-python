from django.db import models
import datetime
from django.utils import timezone

class Model(models.Model):
   user = models.ForeignKey('User', on_delete=models.CASCADE)
   eyes_color = models.CharField(max_length=64)
   hair_color = models.CharField(max_length=64)
   survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
   user_username = models.CharField(max_length=500)

   def save(self, *args, **kwargs):
      if not self.id:
         self.eyes_color = "-"
         self.hair_color = "-"
      return super(Model, self).save(*args, **kwargs)

class User(models.Model):
   username = models.CharField(max_length=48, primary_key=True, unique=True)
   password = models.CharField(max_length=48)
   PHOTOGRAPHER = 'P'
   MODEL = 'M'
   ADMIN = 'A'
   ROLES = [
      (PHOTOGRAPHER, 'Photographer'),
      (MODEL, 'Model'),
      (ADMIN, 'Admin'),
   ]
   role = models.CharField(max_length=1, choices=ROLES, default=MODEL)
   main_photo_url = models.URLField(blank=True, null=True)
   avg_rate = models.FloatField()

   def save(self, *args, **kwargs):
      if not self.id:
         self.avg_rate = 0.0
      return super(User, self).save(*args, **kwargs)

class Notification(models.Model):
   added_date = models.DateTimeField()
   content = models.TextField(max_length=500)
   read_value = models.IntegerField()
   user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

   def save(self, *args, **kwargs):
      if not self.id:
         self.added_date = timezone.now()
         self.read_value = 0
      return super(Notification, self).save(*args, **kwargs)

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

class Photographer(models.Model):
   user = models.ForeignKey('User', on_delete=models.CASCADE)
   survey = models.ForeignKey('Survey', on_delete=models.CASCADE)

class Comment(models.Model):
   rating_user = models.ForeignKey('User', related_name='rating_user', on_delete=models.SET_NULL, null=True)
   rated_user = models.ForeignKey('User', related_name='rated_user', on_delete=models.SET_NULL, null=True)
   added_date = models.DateTimeField()
   content = models.TextField()

   def save(self, *args, **kwargs):
      if not self.id:
         self.added_date = timezone.now()
      return super(Comment, self).save(*args, **kwargs)

class Photoshoot(models.Model):
   invited_user = models.ForeignKey('User', related_name='invited_user', on_delete=models.SET_NULL, null=True)
   inviting_user = models.ForeignKey('User', related_name='inviting_user', on_delete=models.SET_NULL, null=True)
   CREATED = 'C'
   ACCEPTED = 'A'
   CANCELED = 'D'
   ENDED = 'E'
   ROLES = [
      (CREATED, 'Created'),
      (ACCEPTED, 'Accepted'),
      (CANCELED, 'Canceled'),
      (ENDED, 'Ended'),
   ]
   photoshoot_status = models.CharField(max_length=1, choices=ROLES, default=CREATED)
   topic = models.CharField(max_length=64)
   notes = models.TextField()
   meeting_date = models.DateTimeField()
   duration = models.DurationField()
   city = models.CharField(max_length=128)
   street = models.CharField(max_length=128)
   house_number = models.CharField(max_length=64)

class Portfolio(models.Model):
   user = models.ForeignKey('User', on_delete=models.CASCADE)
   name = models.CharField(max_length=32)
   description = models.TextField()
   main_photo_url = models.URLField()
   added_date = models.DateTimeField()

   def save(self, *args, **kwargs):
      if not self.id:
         self.added_date = timezone.now()
      return super(Portfolio, self).save(*args, **kwargs)

class Image(models.Model):
   portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE)
   file_url = models.URLField()
   name = models.CharField(max_length=32)
   added_date = models.DateTimeField()

   def save(self, *args, **kwargs):
      if not self.id:
         self.added_date = timezone.now()
      return super(Image, self).save(*args, **kwargs)
