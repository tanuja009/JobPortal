from django.contrib import admin
from .models import Job,Contact,Post_Info

# Register your models here.
@admin.register(Job)
class Job_Model(admin.ModelAdmin):
  list_display=['id','title','company','location','description','date_posted']

@admin.register(Contact)
class Contact_model(admin.ModelAdmin):
  list_display=['id','massege','name','email','subject']

@admin.register(Post_Info)
class Post_Info_model(admin.ModelAdmin):
  list_display=['id','username','post_img','desc','posted_at']


