from django.db import models
from django.contrib.auth.models import User

# Create

class uploadedfile(models.Model):
  file=models.FileField(upload_to='uploads/')
  upload_at=models.DateField(auto_now_add=True)

  def __str__(self):
    return self.file.name
  
class Post_Info(models.Model):
    username= models.ForeignKey(User ,on_delete=models.CASCADE)
    post_img= models.ImageField(upload_to='post_images/')
    desc= models.TextField()
    posted_at =models.DateTimeField(auto_now_add=True)
  

class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
  
class Contact(models.Model):
   massege=models.TextField()
   name=models.CharField(max_length=50)
   email=models.EmailField(max_length=50,unique=True)
   subject=models.CharField(max_length=50)


class Comment(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   post=models.ForeignKey(Post_Info,on_delete=models.CASCADE)
   content=models.TextField()
   content_at=models.DateTimeField(auto_now_add=True)
