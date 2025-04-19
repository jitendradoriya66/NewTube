from django.db import models

# Create your models here.
class User(models.Model):
    photo=models.ImageField(upload_to='dp',blank=True,null=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    otp=models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.username
    
class category(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    like=models.IntegerField(default=0,blank=True,null=True)
    view=models.IntegerField(default=0,blank=True,null=True)
    category=models.ForeignKey(category,on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.title

class watchLetter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    like=models.IntegerField(default=0,blank=True,null=True)
    view=models.IntegerField(default=0,blank=True,null=True)
    category=models.ForeignKey(category,on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.title

    
# Comments model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} on {self.video.title}'

# Likes/Dislikes model
class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Subscription(models.Model):
        subscriber = models.ForeignKey(User, on_delete=models.CASCADE,related_name='subscription')
        channle=models.ForeignKey(User, on_delete=models.CASCADE ,related_name='subscribers' )
        subscribed_at = models.DateTimeField(auto_now_add=True)
        