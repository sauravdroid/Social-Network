from django.contrib import admin
from .models import Post, PostComment, PostLikes

admin.site.register(Post)
admin.site.register(PostLikes)
admin.site.register(PostComment)
