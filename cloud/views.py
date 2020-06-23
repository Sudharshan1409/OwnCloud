from django.shortcuts import render, redirect
from django.views.generic import TemplateView,DetailView,CreateView,DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import CloudFolder,CloudData
from .serializer import DataSerializer, FolderSerializer
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
    # parser_classes = (MultiPartParser, FormParser)
    # queryset = CloudData.objects.all()

    # template_name = 'cloud/item.html'
    # Removing the line below shows the APIview instead of the template.
    # renderer_classes = [TemplateHTMLRenderer]

    def post(self, request):
        CloudData.objects.create(profile=UserProfile.objects.get(pk=request.POST['profile']),data=request.FILES['data'],folder=CloudFolder.objects.get(pk=request.POST['folder']))
        return redirect(request.POST['backref'])


class AddFolderAPI(LoginRequiredMixin,View):
    # parser_classes = (MultiPartParser, FormParser)
    # queryset = CloudFolder.objects.all()

    # template_name = 'cloud/item.html'
    # Removing the line below shows the APIview instead of the template.
    # renderer_classes = [TemplateHTMLRenderer]

    def post(self, request):
        parent = CloudFolder.objects.get(pk=request.POST['parent_folder'])
        path = parent.path + request.POST['name'] + '/'
        CloudFolder.objects.create(profile=UserProfile.objects.get(pk=request.POST['profile']),name=request.POST['name'],parent_folder=parent, path=path)
        return redirect(request.POST['backref'])
