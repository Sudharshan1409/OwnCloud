from django.shortcuts import render
from django.views.generic import TemplateView,DetailView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import CloudFolder,CloudData
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializer import DataSerializer, FolderSerializer
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from django.contrib import messages
from rest_framework.renderers import TemplateHTMLRenderer
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

class AddFileAPI(LoginRequiredMixin, APIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = CloudData.objects.all()

    template_name = 'cloud/added_item.html'
    # Removing the line below shows the APIview instead of the template.
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request):
        file_serializer = DataSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            response = Response({'data':'file', 'link':request.data['backref']}, status=status.HTTP_201_CREATED)
        else:
            response = Response({'data':file_serializer.errors, 'link':request.data['backref']}, status=status.HTTP_400_BAD_REQUEST)
        return response

class AddFolderAPI(LoginRequiredMixin, APIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = CloudFolder.objects.all()

    template_name = 'cloud/added_item.html'
    # Removing the line below shows the APIview instead of the template.
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request):
        folder_serializer = FolderSerializer(data=request.data)
        if folder_serializer.is_valid():
            folder_serializer.save()
            response = Response({'data':'folder', 'link':request.data['backref']}, status=status.HTTP_201_CREATED)
        else:
            response = Response({'data':folder_serializer.errors, 'link':request.data['backref']}, status=status.HTTP_400_BAD_REQUEST)
        return response
