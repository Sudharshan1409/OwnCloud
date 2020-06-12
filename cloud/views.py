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

    def post(self, request):
        # serializer = DataSerializer(data=request.data)
        # print(request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response('success')
        file_serializer = DataSerializer(data=request.data)
        print(request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            response = Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response
