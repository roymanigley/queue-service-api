from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager

from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        organization_name = input('Organization: ')
        organization = Organization.objects.get_or_create(name=organization_name)[0]
        user = self.model(**extra_fields, organization=organization)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)

class UserProfile(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    objects = UserProfileManager()

    def __str__(self):
        return self.username + ' ' + self.organization.name

    USERNAME_FIELD = 'username'