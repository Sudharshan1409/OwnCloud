from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete,post_save,pre_save
from django.shortcuts import reverse
from django.contrib.auth.models import User
from users.models import UserProfile
from django.shortcuts import get_object_or_404
from users.exception import StorageFullException

def user_directory_path(instance, filename):
    return 'cloud/{0}/{1}'.format(instance.profile.user.username, filename)

class Cloud(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name = 'clouds')
    title = models.CharField(max_length = 128)
    data = models.FileField(upload_to = user_directory_path)
    description = models.TextField(blank = True)

    def __str__ (self):
        return f"{self.profile.user.username.capitalize()} Cloud"

@receiver(post_delete, sender=Cloud)
def submission_delete(sender, instance, **kwargs):
    """
    This function is used to delete attachments when a file object is deleted.
    Django does not do this automatically.
    """
    instance.data.delete(False)


@receiver(post_save,sender=Cloud)
def update_size(sender,instance,created, **kwargs):
    if created:
        profile = instance.profile
        profile.used_size += (instance.data.size/1024)/1024
        profile.percentage_used = (profile.used_size/5120) * 100
        profile.save()

@receiver(pre_save,sender=Cloud)
def allowed_to_upload(sender,instance,**kwargs):
    profile = instance.profile
    if (profile.used_size + (instance.data.size/1024)/1024) > 5120:
        raise StorageFullException('Memory Full in your cloud')
