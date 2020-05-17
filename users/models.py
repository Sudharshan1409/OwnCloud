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
    percentage_used = models.FloatField(default = 0)



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

# print(Cloud)
