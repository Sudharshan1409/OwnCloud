from rest_framework import serializers
from .models import CloudData,CloudFolder



class DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloudData
        fields = '__all__'

class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = CloudFolder
        fields = ('profile','name','parent_folder',)

    def create(self, validated_data):
        folder = CloudFolder(
            profile=validated_data['profile'],
            name=validated_data['name'],
            parent_folder=validated_data['parent_folder']
        )
        folder.path = folder.parent_folder.path + folder.name + '/'
        folder.save()
        return folder
