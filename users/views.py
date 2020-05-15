from django.shortcuts import render
from django.views.generic import TemplateView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from django.contrib.auth.models import User
from .forms import UserForm,UserUpdateForm
from django.urls import reverse,reverse_lazy
from django.utils.decorators import method_decorator
from .decorators import should_not_be_logged_in

# Create your views here.

class UserHomePage(LoginRequiredMixin,TemplateView):
    template_name = 'users/home.html'

@method_decorator(should_not_be_logged_in,name = 'dispatch')
class RegisterUserPage(CreateView):
    template_name = 'users/user_form.html'
    context_object_name = 'form'
    model = User
    form_class = UserForm

    def get_success_url(self):
        return reverse('users:login')

class UpdateUserPage(UpdateView):
    template_name = 'users/user_form.html'
    context_object_name = 'form'
    model = User
    form_class = UserUpdateForm
    def get_success_url(self):
        return reverse_lazy("users:home")
