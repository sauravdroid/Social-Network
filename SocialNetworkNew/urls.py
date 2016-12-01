from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^post/',include('Post.urls')),
    url(r'^user/', include('User.urls')),
    url(r'^admin/', admin.site.urls),
]
