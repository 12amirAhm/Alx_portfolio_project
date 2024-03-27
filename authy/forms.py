from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from authy.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


from django import forms
from django.forms import ModelForm




# class ChatMessageForm(ModelForm):
#     body = forms.CharField(widget=forms.Textarea(attrs={"class":"forms", "rows":3, "placeholder": "Type message here"}))
#     class Meta:
#         model = ChatMessage
#         fields = ["body",]



class UserForm(ModelForm):
    profile_info = forms.CharField(widget=forms.Textarea(attrs={"class":"form__group",  "placeholder": "Write Your Bio here ...."}))
    class Meta:
        model = Profile
        fields = ['picture', 'first_name', 'field_name', 'profile_info', 'location', 'email', 'Phone', 'url']



def ForbiddenUsers(value):
	forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete', 'signup','username']
	if value.lower() in forbidden_users:
		raise ValidationError('Invalid name for username, Try another one.')

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value or '0' in value or '1' in value or '2' in value or '3' in value or '9' in value:
		raise ValidationError('Invalid username, Do not use these chars: @ , - , +  Or Numbers')

# def UniqueEmail(value):
# 	if User.objects.filter(email__iexact=value).exists():
# 		raise ValidationError('User with this email already exists.')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('Username already exists, Try another Username.')

class SignupForm(UserCreationForm):
	# username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True,)
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'prompt srch_explore'}), max_length=10, required=True)
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'prompt srch_explore'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'prompt srch_explore'}))
	# password = forms.CharField(widget=forms.PasswordInput())
	# confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm your password.")

	class Meta:

		model = User
		fields = ('username', 'password1','password2')

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(ForbiddenUsers)
		self.fields['username'].validators.append(InvalidUser)
		self.fields['username'].validators.append(UniqueUser)
		

	def clean(self):
		super(SignupForm, self).clean()
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('confirm_password')

		if password != password2:
			self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
		return self.cleaned_data

# class ChangePasswordForm(UserCreationForm):
# 	id = forms.CharField(widget=forms.HiddenInput())
# 	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Old password", required=True)
# 	new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="New password", required=True)
# 	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Confirm new password", required=True)

# 	class Meta:
# 		model = User
# 		fields = ('id', 'old_password', 'new_password', 'confirm_password')

# 	def clean(self):
# 		super(ChangePasswordForm, self).clean()
# 		id = self.cleaned_data.get('id')
# 		old_password = self.cleaned_data.get('old_password')
# 		new_password = self.cleaned_data.get('new_password')
# 		password2 = self.cleaned_data.get('confirm_password')
# 		user = User.objects.get(pk=id)
# 		if not user.check_password(old_password):
# 			self._errors['old_password'] =self.error_class(['Old password do not match.'])
# 		if new_password != password2:
# 			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
# 		return self.cleaned_data

# class EditProfileForm(forms.ModelForm):
# 	picture = forms.ImageField(required=False)
# 	coverpage = forms.ImageField(required=False)
# 	first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=True)
# 	field_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=True)
# 	location = forms.CharField(widget=forms.TextInput(), max_length=25, required=True)
# 	email = forms.EmailField(widget=forms.TextInput(), max_length=50, required=False)
# 	Phone = forms.IntegerField(widget=forms.NumberInput,  required=False)
# 	url = forms.URLField(widget=forms.TextInput(), max_length=60, required=False)
# 	profile_info = forms.CharField(widget=forms.TextInput(), max_length=360, required=False)

# 	class Meta:
# 		model = Profile
# 		fields = ('picture', 'first_name', 'field_name', 'location', 'email', 'Phone', 'url', 'profile_info')
  
# class EditProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['picture','first_name','last_name','location','url','profile_info']
        