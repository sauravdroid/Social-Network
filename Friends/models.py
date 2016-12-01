from __future__ import unicode_literals

from django.db import models
from User.models import CustomUser


class Friend(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_email = models.EmailField(max_length=255)
    friend_email = models.EmailField(max_length=255)
    friend_type = models.CharField(max_length=50)
    request_type = models.CharField(max_length=20)
    friend_since = models.DateTimeField(null=True)

    class Meta:
        unique_together = (('user_email', 'friend_email'), ('friend_email', 'user_email'))

    def __str__(self):
        return self.user_email + " -> " + self.friend_email + "  || Status : " + self.request_type + " ||"

    def get_friend_username(self):
        return self.friend_email.split('@')[0]

    def get_username(self):
        return self.user_email.split('@')[0]


class RequestList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_email = models.EmailField(max_length=255)
    requested_user_email = models.EmailField(max_length=255)
    request_date = models.DateTimeField()
    request_type = models.CharField(max_length=20)

    class Meta:
        unique_together = (('user_email', 'requested_user_email'),
                           ('requested_user_email', 'user_email'))

    def __str__(self):
        return self.user_email + " || Request from -> " + self.requested_user_email + "  || Status : " + self.request_type + " ||"

    def get_username(self):
        return self.requested_user_email.split('@')[0]
