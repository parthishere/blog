from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse


# Create your models here.


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=150, verbose_name="Add Title")
    text = models.TextField(verbose_name="Descreption")
    created_date = models.DateField(default=timezone.now, verbose_name="Date")
    published = models.BooleanField(verbose_name="Want to Publish Now?(Otherwise It will save as draft)")
    
    def publish_post(self):
        self.published = True
        self.save()
    
    def get_absolute_url(self):
        return reverse("detail-cbv", kwargs={"pk": self.pk})
    
    
    
    
    def approveded_comments(self):
        return self.comment.filter(approved_comment=True)

    def __str__(self):
        return self.title
    


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment' )
    author = models.CharField(max_length=50)
    text = models.CharField(max_length=100)
    published_date = models.DateField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    
    def approveded_comment(self):
        self.approved_comment = True
        
    def __str__(self):
        return self.author
    
    
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    phone_num = models.CharField(max_length = 12, null=True, blank=True, default=None)
    birth_date = models.CharField(max_length = 12, null=True, blank=True, default=None)
    
    def __str__(self):
        return self.user.name
    
