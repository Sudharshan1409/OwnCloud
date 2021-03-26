from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete,post_save,pre_save,pre_delete
from django.shortcuts import reverse
from django.contrib.auth.models import User
from users.models import UserProfile
from django.shortcuts import get_object_or_404
from users.exception import StorageFullException
import os
from django.conf import settings

def user_directory_path(instance, filename):
    return 'cloud/{0}/{1}'.format(instance.folder.path, filename)

class CloudFolder(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name = 'folders')
    name = models.CharField(max_length = 32)
    path = models.CharField(max_length = 2048, null=True, blank=True)
    parent_folder = models.ForeignKey('self',on_delete = models.CASCADE, related_name='all_folders',blank=True, null = True)


    def __str__(self):
        return f"{self.pk} {self.profile.user.username.capitalize()}'s {self.name} Folder"

class CloudData(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name = 'cloud_datas')
    title = models.CharField(max_length = 32, blank = True)
    data = models.FileField(upload_to = user_directory_path)
    description = models.TextField(blank = True)
    folder = models.ForeignKey(CloudFolder, on_delete=models.CASCADE, related_name='files')

    def filename(self):
        return os.path.basename(self.data.name)

    def __str__ (self):
        return f"{self.pk} {self.profile.user.username.capitalize()} Cloud"

@receiver(post_save, sender = UserProfile)
def create_folder(sender,created,instance, **kwargs):
    if created:
        CloudFolder.objects.create(profile = instance, name = instance.user.username, path = instance.user.username + '/', parent_folder = None)
        print('folder created')

@receiver(pre_delete, sender = CloudFolder)
def before_deletion_of_folder(sender, instance, **kwargs):
    files = instance.files.all()
    # for file in files:
        # file.delete()


@receiver(post_delete, sender=CloudData)
def submission_delete(sender, instance, **kwargs):
    """
    This function is used to delete attachments when a file object is deleted.
    Django does not do this automatically.
    """
    instance.data.delete(False)

@receiver(pre_delete, sender=CloudData)
def before_delete(sender, instance, **kwargs):
    profile = instance.profile
    profile.used_size -= (instance.data.size/1024)/1024
    profile.percentage_used = (profile.used_size/5120) * 100
    profile.save()

@receiver(post_delete, sender = CloudFolder)
def delete_folder(sender,instance, **kwargs):
    
    if instance.path[-1] == '/':
        path = instance.path[:-1]
    else:
        path = instance.path
    print(os.path.join(settings.MEDIA_ROOT, 'cloud', path))
    os.rmdir(os.path.join(settings.MEDIA_ROOT, 'cloud', path))
    


@receiver(post_save,sender=CloudData)
def update_size(sender,instance,created, **kwargs):
    if created:
        profile = instance.profile
        profile.used_size += (instance.data.size/1024)/1024
        profile.percentage_used = (profile.used_size/5120) * 100
        profile.save()

@receiver(pre_save,sender=CloudData)
def allowed_to_upload(sender,instance,**kwargs):
    profile = instance.profile
    if (profile.used_size + (instance.data.size/1024)/1024) > 5120:
        raise StorageFullException('Memory Full in your cloud')
