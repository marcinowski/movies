from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth import urls

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^profile/$', TemplateView.as_view(template_name='users/profile.html')),
]
