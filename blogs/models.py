from django.db import models
from accounts.models import *
from django.utils import timezone
# Create your models here.

class Topics(models.Model):
    topic=models.CharField(max_length=100)
    is_block=models.BooleanField(default=False)
    desc = models.CharField(max_length=100,default = 'topic desc')
    img = models.ImageField(upload_to='topic_img/',null=True,blank=True)

    
    def __str__(self):
        return self.topic



class Blogs(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    banner_img=models.ImageField(upload_to='post_banner_img/',null=True,blank=True)
    content=models.TextField()
    topic=models.ForeignKey(Topics,on_delete=models.CASCADE,related_name='blogs',null=True)
    video_post=models.FileField(upload_to='blog_video/',null=True,blank=True)
    is_block=models.BooleanField(default=False)
    likes=models.IntegerField(default=0)
    is_premium_blog=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)
    is_hide = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE,related_name='comments')
    parent_comment=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='replies')
    content=models.TextField()
    likes=models.IntegerField(default=0)
    created_at=models.DateTimeField(default=timezone.now,editable=False)
    updated_at=models.DateTimeField(default=timezone.now,editable=False)

    def __str__(self):
        return f"Comment by {self.user.first_name} on {self.blog.title}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'blog']

    def __str__(self):
        return f"{self.user.first_name} likes {self.blog.title}"


class Report_blog(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    reason=models.CharField(max_length=250)
    reported_at=models.DateTimeField(default=timezone.now,editable=False)
    is_solved=models.BooleanField(default=False)



class SavedBlogs(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('user','blog')
    

    def __str__(self) -> str:
        return f'{self.user.first_name} saved {self.blog.title}'


class Community(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    image=models.ImageField(upload_to='community_img/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)