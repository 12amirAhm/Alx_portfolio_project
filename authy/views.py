from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, UserForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from comment.models import Comment
from authy.models import Profile
from post.models import Post, Follow, Stream
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.urls import resolve


from django.shortcuts import render, redirect
from .models import  Profile

 

def error_404_view(request,exception):
    return render(request,'404.html')

# Create your views here.
# def index(request):
#     user = request.user.profile
#     friends = user.friends.all()
#     context = {"user": user, "friends": friends}
#     return render(request, "newmessage.html", context)


# def detail(request,pk):
#     friend = Friend.objects.get(profile_id=pk)
#     user = request.user.profile
#     profile = Profile.objects.get(id=friend.profile.id)
#     chats = ChatMessage.objects.all()
#     rec_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user, seen=False)
#     rec_chats.update(seen=True)
#     form = ChatMessageForm()
#     if request.method == "POST":
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             chat_message.msg_sender = user
#             chat_message.msg_receiver = profile
#             chat_message.save()
#             return redirect("detail", pk=friend.profile.id)
#     context = {"friend": friend, "form": form, "user":user, 
#                "profile":profile, "chats": chats, "num": rec_chats.count()}
#     return render(request, "detail.html", context)

# def sentMessages(request, pk):
#     user = request.user.profile
#     friend = Friend.objects.get(profile_id=pk)
#     profile = Profile.objects.get(id=friend.profile.id)
#     data = json.loads(request.body)
#     new_chat = data["msg"]
#     new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile, seen=False )
#     print(new_chat)
#     return JsonResponse(new_chat_message.body, safe=False)

# def receivedMessages(request, pk):
#     user = request.user.profile
#     friend = Friend.objects.get(profile_id=pk)
#     profile = Profile.objects.get(id=friend.profile.id)
#     arr = []
#     chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
#     for chat in chats:
#         arr.append(chat.body)
#     return JsonResponse(arr, safe=False)

# def chatNotification(request):
#     user = request.user.profile
#     friends = user.friends.all()
#     arr = []
#     for friend in friends:
#         chats = ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
#         arr.append(chats.count())
#     return JsonResponse(arr, safe=False)


@login_required(login_url='login')
def updateUser(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    form = UserForm(instance=profile)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)

    return render(request, 'authy/update-user.html', {'form': form})

# Create your views here.
@login_required(login_url='register')
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name
	all_users = User.objects.all().order_by('-date_joined')

	commentNo = Comment.objects.all().count()
	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')

	else:
		posts = profile.favorites.all()

	#Profile info box
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	#follow status
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	#Pagination
	paginator = Paginator(posts, 50)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
     
		'posts': posts_paginator,
		'profile':profile,
    	'all_users': all_users,
        'commentNo': commentNo,
		'following_count':following_count,
		'followers_count':followers_count,
		'posts_count':posts_count,
		'follow_status':follow_status,
		'url_name':url_name,
	}

	return HttpResponse(template.render(context, request))

@login_required(login_url='register')
def UserProfileFavorites(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	
	
	posts = profile.favorites.all('-created')

	#Profile info box
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	#Pagination 
	paginator = Paginator(posts, 50)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile_favorite.html')

	context = {
		'posts': posts_paginator,
		'profile':profile,
       
		'following_count':following_count,
		'followers_count':followers_count,
		'posts_count':posts_count,
	}

	return HttpResponse(template.render(context, request))


def Signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Profile.get_or_create(user=request.user)
           
            

            # Automatically Log In The User
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            # return redirect('editprofile')
            return redirect('index')
            


    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)

# def Signup(request):
# 	if request.method == 'POST':
# 		form = SignupForm(request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data.get('username')
			
# 			password = form.cleaned_data.get('password')
# 			User.objects.create_user(username=username, password=password)
# 			return redirect('index')
# 	else:
# 		form = SignupForm()
	
# 	context = {
# 		'form':form,
# 	}

# 	return render(request, 'signup.html', context)


# @login_required
# def PasswordChange(request):
# 	user = request.user
# 	if request.method == 'POST':
# 		form = ChangePasswordForm(request.POST)
# 		if form.is_valid():
# 			new_password = form.cleaned_data.get('new_password')
# 			user.set_password(new_password)
# 			user.save()
# 			update_session_auth_hash(request, user)
# 			return redirect('change_password_done')
# 	else:
# 		form = ChangePasswordForm(instance=user)

# 	context = {
# 		'form':form,
# 	}

# 	return render(request, 'change_password.html', context)

# def PasswordChangeDone(request):
# 	return render(request, 'change_password_done.html')


# @login_required
# def EditProfile(request):
# 	user = request.user.id
# 	profile = Profile.objects.get(user__id=user)
# 	BASE_WIDTH = 400

# 	if request.method == 'POST':
# 		form = EditProfileForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			profile.picture = form.cleaned_data.get('picture')
# 			profile.coverpage = form.cleaned_data.get('coverpage')
# 			profile.first_name = form.cleaned_data.get('first_name')
# 			profile.field_name = form.cleaned_data.get('field_name')
# 			profile.location = form.cleaned_data.get('location')
# 			profile.url = form.cleaned_data.get('url')
# 			profile.email = form.cleaned_data.get('email')
# 			profile.Phone = form.cleaned_data.get('Phone')
# 			profile.Are_You_Business = form.cleaned_data.get('Are_You_Business')
			
# 			profile.profile_info = form.cleaned_data.get('profile_info')
# 			profile.save()
# 			return redirect('index')
# 	else:
# 		form = EditProfileForm()

# 	context = {
# 		'form':form,
# 	}

# 	return render(request, 'authy/edit_profile.html', context)




	


# @login_required
# def follow(request, username, option):
#     user = request.user
#     following = get_object_or_404(User, username=username)
#     try:
#         f, created = Follow.objects.get_or_create(follower=request.user, following=following)
        
#         if int(option) == 0:
#             f.delete()
#             Stream.objects.filter(following=following, user=user).all().delete()
            
#         else:
#             posts = Post.objects.all().filter(user=following)[:10]
            
            
#             with transaction.atomic():
#                 for post in posts:
#                     stream = Stream(post=post, user=user, date=post.posted, following=following)
#                     stream.save()
                    
                
                    
#         return HttpResponseRedirect(reverse('profile', args=[username]))
#     except User.DoesNotExist:
#         return HttpResponseRedirect(reverse('profile', args=[username])) 
    
 
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

               