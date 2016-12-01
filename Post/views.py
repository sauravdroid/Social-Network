from django.shortcuts import render
from django.http import HttpResponse
from .forms import CommentForm
from .models import Post
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from .models import PostComment
from django.contrib.auth.decorators import login_required


@login_required(login_url='user:login')
def get_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=post_id)
        post_comments = post.postcomment_set.all().order_by('-comment_at')
        form = CommentForm()
        return render(request, 'Post/comment.html',
                      {"form": form, "title": post.title, "comments": post_comments, "email": request.user.email,
                       "username": request.user.get_username()})
        # return redirect('post:get_post', post_id=post_id)
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_post = form.save(commit=False)
            comment_post.user = request.user
            comment_post.post = get_object_or_404(Post, id=post_id)
            comment_post.comment_at = timezone.now()
            comment_post.save()
            # return redirect('user:profile', user_email=request.user.email)
            return redirect('post:get_post', post_id=post_id)
