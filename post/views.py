from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from post.models import Stream, Post, Follow, Tag , Likes, Job, Jobtitle, Workplace, Video, VStream,PostFileContent
from post.forms import JobForm, NewPostForm
# from stories.models import Story, StoryStream
from django.core.paginator import Paginator
from django.http import JsonResponse

from comment.models import Comment
from comment.forms import CommentForm
from django.db.models import Q

from django.contrib.auth.decorators import login_required

from django.urls import reverse
from authy.models import Profile

from django.contrib.auth.models import User
from django.db import transaction


def handle(request, exception):
    return render(request, '404.html', {})



@login_required(login_url='login')
def Privacy(request):
    return render(request, 'post/privacy.html')



def Terms(request):
    return render(request, 'post/terms.html')

@login_required(login_url='login')
def Transition(request):
    return render(request, 'post/our_service.html')

@login_required(login_url='login')
def monitize(request):
 return render(request, 'post/monitize.html')

@login_required(login_url='login')
def Switch(request):
    return render(request, 'post/switch.html')

@login_required(login_url='login')
def postpro(request):
    return render(request, 'post/postpro.html')

@login_required(login_url='login')
def About(request):
    return render(request, 'post/aboutus.html')

@login_required(login_url='login')
def Propost(request):
    return render(request, 'post/postprice.html')

@login_required(login_url='login')
def Payjob(request):
    return render(request, 'post/payjob.html')


@login_required(login_url='login')
def Paybuss(request):
    return render(request, 'post/paybuss.html')


@login_required(login_url='login')
def Payblue(request):
    return render(request, 'post/payblue.html')



@login_required
def UserSearch(request):
	query = request.GET.get("q")
	context = {}
	

	if query:
		users = User.objects.filter(Q(username__icontains=query))

		#Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)
		followers_count = Follow.objects.filter(following=page_number).count()
		context = {
				'users': users_paginator,
                'followers_count':followers_count,
			}
	
	template = loader.get_template('search_tofo.html')
	
	return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def Vacancy(request):
   
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    jobs = Job.objects.filter(
        Q(JobTitle__titlename__icontains=q) |
        Q(Work_Place__woplace__icontains=q)
       
      
    )
    
    
    job_count = jobs.count()
    jobtitles = Jobtitle.objects.all()[0:10]
    workplaces = Workplace.objects.all()[0:5]
 
    context = {'jobs': jobs, 'job_count':job_count, 'jobtitles': jobtitles, 'workplaces': workplaces ,}
    return render(request, 'post/vacancy.html', context)


@login_required(login_url='signup')
def jobs(request, pk):
    job = Job.objects.get(id=pk)

    candidates = job.candidates.all()
   
    
 
    if request.method == 'POST':
       
        job.candidates.add(request.user)
        messages.success(request, ' Request Sent !!! Follow up Your Inbox you maybe contacted by the Employeer')
        return redirect('jobs', pk=job.id)
   
    context = {
              'candidates': candidates,
             
                'job':job
                
              }
    return render(request, 'post/jobs.html', context)

@login_required(login_url='signup')
def createJob(request):
    form = JobForm()
    jobtitles = Jobtitle.objects.all()
    workplaces = Workplace.objects.all()
    if request.method == 'POST':
        jobtitle_name = request.POST.get('jobtitle')
        workplace_name = request.POST.get('workplace')
        jobtitle, created = Jobtitle.objects.get_or_create(titlename=jobtitle_name)
        workplace, created = Workplace.objects.get_or_create(woplace=workplace_name)

        Job.objects.create(
            user=request.user,
            JobTitle=jobtitle,
            Work_Place=workplace,
            Job_Description=request.POST.get('Job_Description'),
            Quantity=request.POST.get('Quantity'),
            Salary=request.POST.get('Salary'),
            Employment_Status=request.POST.get('Employment_Status'),
            Additional_Requirments=request.POST.get('Additional_Requirments'),
            How_to_Apply=request.POST.get('How_to_Apply'),
            Dead_Line=request.POST.get('Dead_Line'),
           
        )
        return redirect('vacancy')
 
    context = {'form': form, 'jobtitles': jobtitles, 'workplaces' : workplaces}
    return render(request, 'post/job_form.html', context)



@login_required(login_url='login')
def deleteJob(request, pk):
    job = Job.objects.get(id=pk)

    if request.user != job.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        job.delete()
        return redirect('vacancy')
    return render(request, 'post/deletejob.html', {'obj': job})



@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)

    if request.user != post.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        post.delete()
        return redirect('index')
    return render(request, 'post/deletepost.html', {'obj': post})




@login_required(login_url='signup')
def updateJob(request, pk):
    job = Job.objects.get(id=pk)
    form = JobForm(instance=job)
    jobtitles = Jobtitle.objects.all()
    workplaces = Workplace.objects.all()
    if request.user != job.user:
            return HttpResponse('Your are not allowed here!!')
        
    if request.method == 'POST':
             jobtitle_name = request.POST.get('jobtitle')
             workplace_name = request.POST.get('workplace')
             jobtitle, created = Jobtitle.objects.get_or_create(titlename=jobtitle_name)
             workplace, created = Workplace.objects.get_or_create(woplace=workplace_name)
             job.JobTitle = jobtitle
             job.Work_Place = workplace
             job.Job_Description=request.POST.get('Job_Description')
             job.Quantity=request.POST.get('Quantity')
             job.Salary=request.POST.get('Salary')
             job.Employment_Status=request.POST.get('Employment_Status')
             job.Additional_Requirments=request.POST.get('Additional_Requirments')
             job.How_to_Apply=request.POST.get('How_to_Apply')
             job.Dead_Line=request.POST.get('Dead_Line')
             job.save()
             return redirect('vacancy')

    context = {'form': form, 'job': job, 'jobtitles': jobtitles, 'workplaces' : workplaces}
    return render(request, 'post/job_form.html', context)



# # Create your views here.
@login_required(login_url='signup')
def index(request):
	user = request.user
	posts = Stream.objects.filter(user=user)
	all_users = User.objects.all().order_by('-date_joined')	
	all_peoples = User.objects.all().order_by('date_joined')	
	
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
	profile = Profile.objects.all()
	postin = Post.objects.filter(user=user).order_by('-posted')
	
	# commentNo = Comment.objects.filter(user=Stream).count()
	# # stories = StoryStream.objects.filter(user=user)
	

	group_ids = []

	for post in posts:
		group_ids.append(post.post_id)
  
	for post in postin:
		group_ids.append(post.id)
		
	post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
	post_ins = Post.objects.filter(id__in=group_ids).all().order_by('-posted')


	template = loader.get_template('post/index.html')

	context = {
		'postins': post_ins,
     	'posts': posts_paginator,
		'post_items': post_items,
        'follow_status': follow_status,
        'profile': profile,
        'all_users': all_users,
        'all_peoples': all_peoples,
        'following_count':following_count,
		'followers_count':followers_count,
       
		# 'stories': stories,

	}

	return HttpResponse(template.render(context, request))




# # Create your views here.
@login_required(login_url='signup')
def indextwo(request):
	user = request.user
	posts = Stream.objects.filter(user=user)
	all_users = User.objects.all().order_by('-date_joined')	
	all_peoples = User.objects.all().order_by('date_joined')	
	
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
	profile = Profile.objects.all()
	
	# commentNo = Comment.objects.filter(user=Stream).count()
	# # stories = StoryStream.objects.filter(user=user)
	

	group_ids = []

	for post in posts:
		group_ids.append(post.post_id)
		
	post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')		


	template = loader.get_template('post/indextwo.html')

	context = {
     	'posts': posts_paginator,
		'post_items': post_items,
        'follow_status': follow_status,
        'profile': profile,
        'all_users': all_users,
        'all_peoples': all_peoples,
        'following_count':following_count,
		'followers_count':followers_count,
       
		# 'stories': stories,

	}

	return HttpResponse(template.render(context, request))















# @login_required(login_url='signup')
# def video(request):
# 	user = request.user
# 	videos = VStream.objects.filter(user=user)

# 	# stories = StoryStream.objects.filter(user=user)


# 	group_ids = []

# 	for video in videos:
# 		group_ids.append(video.video_id)
		
# 	video_items = Video.objects.filter(id__in=group_ids).all().order_by('-vposted')		

# 	template = loader.get_template('post/video.html')

# 	context = {
# 		'video_items': video_items,
# 		# 'stories': stories,

# 	}

# 	return HttpResponse(template.render(context, request))

@login_required
def PostDetails(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	user = request.user
	profile = Profile.objects.get(user=user)
	favorited = False

	# #comment
	comments = Comment.objects.filter(post=post).order_by('-date')
	commentNo = Comment.objects.filter(post=post).count()
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=user)
	# 	#For the color of the favorite button

		if profile.favorites.filter(id=post_id).exists():
			favorited = True

	# #Comments Form
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.user = user
			comment.save()
			return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
	else:
		form = CommentForm()


	template = loader.get_template('post_detail.html')

	context = {
		'post':post,
		'favorited':favorited,
		'profile':profile,
		'form':form,
		'comments':comments,
		'commentNo':commentNo,
	}

	return HttpResponse(template.render(context, request))

# @login_required(login_url='login')
# def NewPost(request):
#     user = request.user
#     form = SettingForm(instance=user)
#     tags_objs = []
    
#     if request.method == 'POST':
#         form = SettingForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
    
    
    
    

#     if request.method == 'POST':
#         caption = form.cleaned_data.get('caption')
#         tags_form = form.cleaned_data.get('tags')
        
#         tags_list = list(tags_form.split(','))
        
#         for tag in tags_list:
#             t, created = Tag.objects.get_or_create(title=tag)
#             tags_objs.append(t)
       
       
#         p, created = Post.objects.get_or_create(caption=caption, user=user )
#         p.tags.set(tags_objs)
#         p.save()
        
#         return redirect('index')
	

#     return render(request, 'newpost.html', {'form': form })



# @login_required
# def NewPost(request):
# 	user = request.user
# 	tags_objs = []
	
	

# 	if request.method == 'POST':
# 		form = NewPostForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			postpic = form.cleaned_data.get('postpic')
# 			videopic = request.FILES.getlist('videopic')
# 			caption = form.cleaned_data.get('caption')
# 			tags_form = form.cleaned_data.get('tags')

# 			tags_list = list(tags_form.split(','))

# 			for tag in tags_list:
# 				t, created = Tag.objects.get_or_create(title=tag)
# 				tags_objs.append(t)
    
			
	

# 			p, created = Post.objects.get_or_create(postpic=postpic, caption=caption, user=user, videopic=videopic )
# 			p.tags.set(tags_objs)
# 			p.save()
# 			return redirect('index')
# 	else:
# 		form = NewPostForm()

# 	context = {
# 		'form':form,
# 	}

# 	return render(request, 'newpost.html', context)


@login_required
def NewPost(request):
	user = request.user
	tags_objs = []
	files_objs = []

	if request.method == 'POST':
		form = NewPostForm(request.POST, request.FILES)
		if form.is_valid():
			postpic = form.cleaned_data.get('postpic')
			files = request.FILES.getlist('content')
			caption = form.cleaned_data.get('caption')
			tags_form = form.cleaned_data.get('tags')

			tags_list = list(tags_form.split(','))

			for tag in tags_list:
				t, created = Tag.objects.get_or_create(title=tag)
				tags_objs.append(t)

			for file in files:
				file_instance = PostFileContent(file=file, user=user)
				file_instance.save()
				files_objs.append(file_instance)

			p, created = Post.objects.get_or_create(caption=caption, user=user, postpic=postpic)
			p.tags.set(tags_objs)
			p.content.set(files_objs)
			p.save()
			return redirect('index')
	else:
		form = NewPostForm()

	context = {
		'form':form,
	}

	return render(request, 'newpost.html', context)


@login_required(login_url='register')
def tags(request, tag_slug):
	tag = get_object_or_404(Tag, slug=tag_slug)
	posts = Post.objects.filter(tags=tag).order_by('-posted')

	template = loader.get_template('tag.html')

	context = {
		'posts':posts,
		'tag':tag,
	}

	return HttpResponse(template.render(context, request))

 

# @login_required
# def like(request, post_id):
# 	user = request.user
# 	post = Post.objects.get(id=post_id)
# 	current_likes = post.likes
# 	liked = Likes.objects.filter(user=user, post=post).count()

# 	if not liked:
# 		like = Likes.objects.create(user=user, post=post)
# 		like.save()
# 		current_likes = current_likes + 1

# 	else:
# 		Likes.objects.filter(user=user, post=post).delete()
# 		current_likes = current_likes - 1

# 	post.likes = current_likes
# 	post.save()
 
#  return HttpResponseRedirect(reverse('postdetails', args=[post_id]))

# 	return HttpResponseRedirect(reverse('po'))





@login_required 
def like(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	liked = Likes.objects.filter(user=user, post=post).count()

	if not liked:
		like = Likes.objects.create(user=user, post=post)
		#like.save()
		current_likes = current_likes + 1

	else:
		Likes.objects.filter(user=user, post=post).delete()
		current_likes = current_likes - 1

	post.likes = current_likes
	post.save()

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))


@login_required
def favorite(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites.filter(id=post_id).exists():
		profile.favorites.remove(post)

	else:
		profile.favorites.add(post)

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))

@login_required   
def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=request.user, date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))


