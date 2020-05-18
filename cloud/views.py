from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
# Create your views here.

class CloudHomePage(LoginRequiredMixin,TemplateView):
    template_name = 'cloud/home.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user'] = self.request.user
        context['hi'] = 55
        return context

class CloudFileFolderPage(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'cloud/cloud.html'
