from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    url(r'^(?P<post_id>[0-9]+)', views.get_post, name='get_post'),
]
