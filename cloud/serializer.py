from rest_framework import serializers
from .models import CloudData,CloudFolder


class DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloudData
        fields = '__all__'

class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloudFolder
        fields = '__all__'
