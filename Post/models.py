from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from User.models import CustomUser


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now())
    likes = models.IntegerField(default=0)
    liked_at = models.DateTimeField(default=timezone.now())

    class Meta:
        verbose_name = "Post Detail"

    def __str__(self):
        return self.title + " || Likes -> " + str(self.likes)

    def comment_count(self):
        return self.postcomment_set.count()


class PostLikes(models.Model):
    user = models.ForeignKey(CustomUser)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_email = models.EmailField(max_length=255, default='default@gmail.com')
    post_id_meta = models.IntegerField(default=0)
    # likes = models.IntegerField(default=0)
    liked_at = models.DateTimeField(default=timezone.now())

    class Meta:
        verbose_name = "Post Like"
        unique_together = (('user_email', 'post_id_meta'),)

    def __str__(self):
        return self.user.email + " || " + self.post.title + " --> " + str(self.post.likes)


class PostComment(models.Model):
    user = models.ForeignKey(CustomUser)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_at = models.DateTimeField(default=timezone.now())

    class Meta:
        verbose_name = "Post Comment"

    def __str__(self):
        return self.post.title + " --> " + self.comment + " || " + self.user.get_full_name() + " ( " + self.user.email + " )"
