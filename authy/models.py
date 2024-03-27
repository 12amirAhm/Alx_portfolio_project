from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from xmlrpc.client import Boolean
from django.db.models.signals import post_save

from PIL import Image
from django.conf import settings
import os
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
  return  'user_{0}/{1}'.format(instance.user.id, filename)
    
# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	
	first_name = models.CharField(max_length=150, null=True, blank=True)
	golden_checker = models.BooleanField(default=False)
	blue_checker = models.BooleanField(default=False)
	job_checker = models.BooleanField(default=False)
	field_name = models.CharField(max_length=50, null=True, blank=True)
	location = models.CharField(max_length=50, null=True, blank=True)
	url = models.CharField(max_length=80, null=True, blank=True)
	profile_info = models.TextField(max_length=250, null=True, blank=True)
	# Industry = models.ForeignKey(Field, null=True,blank=True, on_delete=models.CASCADE)
	created = models.DateField(auto_now_add=True)
	favorites = models.ManyToManyField(Post)
	email = models.EmailField( null=True, blank=True)
	Phone = models.IntegerField(blank=True,null=True)
	picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Picture')
	coverpage = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='coverpage')
	

		

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)