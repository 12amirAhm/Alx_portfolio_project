import uuid
from django.db import models
from django.contrib.auth.models import User


from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse
from .validators import file_size
from notifications.models import Notification



# Create your models here.


# For direct Announcement Users
class Jobtitle(models.Model):
    titlename = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True )
    created = models.DateTimeField(auto_now_add=True )

    class Meta:
         ordering = ['-updated', '-created']



    def __str__(self):
        return self.titlename

class Workplace(models.Model):
    woplace = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True )
    created = models.DateTimeField(auto_now_add=True )

    class Meta:
         ordering = ['-updated', '-created']



    def __str__(self):
        return self.woplace
    









class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    candidates = models.ManyToManyField(
       User, related_name='candidates', blank=True)
    
    JobTitle = models.ForeignKey(Jobtitle, on_delete=models.SET_NULL, null=True)
    Job_Description = models.TextField(null=True, blank=True) 
    Work_Place = models.ForeignKey(Workplace, on_delete=models.SET_NULL, null=True)
    Employment_Status = models.CharField(max_length=200)
    Salary = models.CharField(max_length=200)
    Quantity = models.CharField(max_length=200)
    Additional_Requirments = models.TextField(null=True, blank=True) 
    How_to_Apply = models.TextField(null=True, blank=True) 
    Dead_Line = models.CharField(max_length=200)
    
    updated = models.DateTimeField(auto_now=True )
    created = models.DateTimeField(auto_now_add=True )

    class Meta:
         ordering = ['-updated', '-created']
         
         
    def __str__(self):
        return self.Dead_Line
    





def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Tag(models.Model):
	title = models.CharField(max_length=75, verbose_name='Tag')
	slug = models.SlugField(null=False, unique=True)

	class Meta:
		verbose_name='Tag'
		verbose_name_plural = 'Tags'

	def get_absolute_url(self):
		return reverse('tags', args=[self.slug])

	
		
	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)

class PostFileContent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner')
	file = models.FileField(upload_to="video/%y", null=False)

# validators=[file_size],
 
class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	postpic =  models.ImageField(upload_to=user_directory_path, verbose_name='Postpic', null=True)
	content =  models.ManyToManyField(PostFileContent, related_name='contents')
	caption = models.TextField(max_length=1500, verbose_name='Caption')
	posted = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, related_name='tags')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.IntegerField(default=0)
	




def get_absolute_url(self):
		     return reverse('postdetails', args=[str(self.id)])

def __str__(self):
	      return str(self.posted)



class Video(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	videopic =  models.FileField(upload_to="video/%y", validators=[file_size], null=False)
	caption = models.TextField(max_length=1500, verbose_name='Caption')
	vposted = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag, related_name='vtags')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	likes = models.IntegerField(default=0)




def get_absolute_url(self):
		     return reverse('postdetails', args=[str(self.id)])

def __str__(self):
	      return str(self.vposted)




class Follow(models.Model):
	follower = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='follower')
	following = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='following')

	def user_follow(sender, instance, *args, **kwargs):
		follow = instance
		sender = follow.follower
		following = follow.following
		notify = Notification(sender=sender, user=following, notification_type=3)
		notify.save()
  
	def user_unfollow(sender, instance, *args, **kwargs):
		follow = instance
		sender = follow.follower
		following = follow.following

		notify = Notification.objects.filter(sender=sender, user=following, notification_type=3)
		notify.delete()





class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()
            	
   

class VStream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='vstream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()
            	
    def add_video(sender, instance, *args, **kwargs):
        video = instance
        user = video.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            vstream = VStream(video=video, user=follower.follower, date=video.vposted, following=user)
            vstream.save()




class Likes(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

	def user_liked_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user
		notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
		notify.save()

	def user_unlike_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
		notify.delete()

#Stream
post_save.connect(Stream.add_post, sender=Post)

#Likes
post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unlike_post, sender=Likes)

#Follow
post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)