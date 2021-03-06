from django.conf.urls import url, include
from users.views import UserProfileView, UserEditProfileView, UserDeleteView, UserCreateView
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'users/logout.html', 'next_page': '/'}, name='logout'),
    url(r'^password_change/$', auth_views.password_change, name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^profile/$', UserProfileView.as_view()),
    url(r'^profile/edit/$', UserEditProfileView.as_view()),
    url(r'^profile/delete/$', UserDeleteView.as_view()),
    url(r'^register/$', UserCreateView.as_view()),
]
