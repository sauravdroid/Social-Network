from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.conf import settings


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, password):
        if not email:
            raise ValueError("You must specify a valid email")
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, date_of_birth, password):
        user = self.create_user(email=email, password=password, first_name=first_name, last_name=last_name,
                                date_of_birth=date_of_birth)
        user.is_admin = True
        user.save()
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    class Meta:
        verbose_name = 'CustomUser'

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_username(self):
        return self.email.split('@')[0]


class ProfileCustomer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about = models.CharField(max_length=500)
    gender = models.CharField(max_length=20)
