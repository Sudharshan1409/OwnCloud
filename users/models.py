from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete,post_save,pre_save
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .exception import StorageFullException

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="users/profile_pics/", blank = True)
    description = models.TextField(blank = True)
    used_size = models.FloatField(default = 0)



    def get_absolute_url(self):
        return reverse('users:home',kwargs = {'pk':self.pk})

    def __str__(self):
        return f"{self.user.username.capitalize()} Profile"

@receiver(post_delete, sender=UserProfile)
def submission_delete(sender, instance, **kwargs):
    """
    This function is used to delete attachments when a file object is deleted.
    Django does not do this automatically.
    """
    instance.profile_pic.delete(False)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)
        print('profile created')

@receiver(post_save,sender=User)
def update_profile(sender,instance,created, **kwargs):
    if not created:
        instance.userprofile.save()
        print('profile updated')

def user_directory_path(instance, filename):
    return 'cloud/{0}/{1}'.format(instance.user.username, filename)

class Cloud(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'clouds')
    title = models.CharField(max_length = 128)
    data = models.FileField(upload_to = user_directory_path)
    description = models.TextField(blank = True)

    def __str__ (self):
        return f"{self.user.username.capitalize()} Cloud {(self.data.size/1024)/1024}"

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
        user = get_object_or_404(User,pk = instance.user.pk)
        profile = user.userprofile
        profile.used_size += (instance.data.size/1024)/1024
        profile.save()

@receiver(pre_save,sender=Cloud)
def allowed_to_upload(sender,instance,created, **kwargs):
    user = get_object_or_404(User,pk = instance.user.pk)
    profile = user.userprofile
    if (profile.used_size + (instance.data.size/1024)/1024) > 5120:
        raise StorageFullException('Memory Full in your cloud')
