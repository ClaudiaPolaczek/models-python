from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
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

    USERNAME_FIELD = 'username'
    #REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.avg_rate = 0.0
        return super(CustomUser, self).save(*args, **kwargs)