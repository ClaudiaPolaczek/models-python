from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, models):
        return True

    @property
    def is_staff(self):
        if self.role == CustomUser.ADMIN:
            return True
        else:
            return False
