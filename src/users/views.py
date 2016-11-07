from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.shortcuts import HttpResponseRedirect


class UserProfileView(TemplateView):
    template_name = 'users/profile.html'


class UserEditProfileView(TemplateView):
    template_name = 'users/edit_profile.html'


class UserDeleteView(TemplateView):
    template_name = 'users/delete_profile.html'


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'users/create_profile.html'
        return render(request, template_name=template_name, context={})

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', '')
        User.objects.create_user(**data)
        return render(request, template_name='users/create_profile_success.html', context={})
