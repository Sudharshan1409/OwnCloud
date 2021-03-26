from django.shortcuts import render, redirect
from django.views.generic import TemplateView,DetailView,CreateView,DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import CloudFolder,CloudData
from django.contrib import messages
from django.urls import reverse
from users.models import UserProfile
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

class CloudFolderPage(LoginRequiredMixin,DetailView):
    model = CloudFolder
    template_name = 'cloud/cloud.html'
    context_object_name = 'cloudfolder'

class AddFileAPI(LoginRequiredMixin,View):

    def post(self, request):
        CloudData.objects.create(profile=UserProfile.objects.get(pk=request.POST['profile']),data=request.FILES['data'],folder=CloudFolder.objects.get(pk=request.POST['folder']))
        return redirect(request.POST['backref'])


class AddFolderAPI(LoginRequiredMixin,View):

    def post(self, request):
        parent = CloudFolder.objects.get(pk=request.POST['parent_folder'])
        path = parent.path + request.POST['name'] + '/'
        CloudFolder.objects.create(profile=UserProfile.objects.get(pk=request.POST['profile']),name=request.POST['name'],parent_folder=parent, path=path)
        return redirect(request.POST['backref'])

class DeleteAPI(LoginRequiredMixin,View):
    
    def post(self, request):
    
        # print(request.POST.get('type'), request.POST.get('pk'), request.POST['backref'])
        if request.POST.get('type') == 'folder':
            folder = CloudFolder.objects.get(pk=request.POST.get('pk'))
            folder.delete()
        else:
            file = CloudData.objects.get(pk=request.POST.get('pk'))
            file.delete()
        return redirect(request.POST['backref'])