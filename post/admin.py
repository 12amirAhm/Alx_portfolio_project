from django.contrib import admin
from post.models import Post, Tag, Follow, Stream, Likes,  Job, Workplace, Jobtitle, Video, VStream, PostFileContent

# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(Likes)
admin.site.register(Jobtitle)
admin.site.register(Job)
admin.site.register(Workplace)
admin.site.register(Video)
admin.site.register(VStream)
admin.site.register(PostFileContent)