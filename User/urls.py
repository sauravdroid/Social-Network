from django.conf.urls import url
from . import views

app_name = 'user'

urlpatterns = [
    url(r'^all/$',views.get_all_users,name='all_user'),
    url(r'^register/$',views.register_user,name='register'),
    url(r'^login/$',views.login_user,name='login'),
    url(r'^logout/',views.logout_user,name='logout'),
    url(r'^profile/(?P<user_email>[\w.@\-]+)/',views.user_profile,name='profile'),
    url(r'^profile/',views.show_profile,name="show_profile"),
    url(r'^create_article$',views.create_article,name='create_article'),
    url(r'^friends',views.show_friends,name='friends'),
]
