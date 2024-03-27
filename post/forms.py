from django import forms
from post.models import Post, Job
from django.forms import ModelForm
from django.forms import ClearableFileInput

# class NewPostForm(forms.ModelForm):
# 	postpic = forms.ImageField(required=False)
# 	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
# 	tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), required=True)
# 	videopic = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)

# 	class Meta: 
# 		model = Post
# 		fields = ('postpic', 'videopic', 'caption', 'tags')
  
class NewPostForm(forms.ModelForm):
    # body = forms.CharField(widget=forms.Textarea(attrs={"class":"forms", "rows":3, "placeholder": "Type message here"}))
	content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
	postpic = forms.ImageField(required=False)
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium', "color":"black", "placeholder": "Enter description here"}), required=True)
	tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium',"placeholder": "Enter Your #Tag here"}), required=True)

	class Meta:
		model = Post
		fields = ('content', 'postpic','caption', 'tags')

# class SettingForm(ModelForm):
#     class Meta:
#         model = Post
#         fields = ['postpic','videopic','caption','tags' ]
        
  
  


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['user']
        