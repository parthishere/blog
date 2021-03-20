from django import forms
from django.contrib.auth import get_user_model


from blog.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author', 'title', 'text', 'created_date', 'published')
    
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('initial', None)
    #     super(PostForm, self).__init__(*args, **kwargs)


class CommentsForm(forms.ModelForm):
    class Meta():
        model = Comment
        exclude = ('approved_comment', 'published_date')
        

class UserProfileInfoForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField(label="Input Email")
    password = forms.CharField(widget=forms.PasswordInput)
    # class Meta():
    #     model = UserProfileInfo
        
    #     exclude = ('last_name',)

user = get_user_model()


class UserRegister(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField(label="Input Email")
    password = forms.CharField(widget=forms.PasswordInput)
    # password2 = forms.CharField(widget=forms.PasswordInput)
    