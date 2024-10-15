from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,View
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout,login
import re
import requests 
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from django.db.models import Q
# SignUp Form
class SignUp(View):
    def post(self, request):
      try:
        print("Inside post method")
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["conf_password"]

        errors = {}
        # Hunter api key for email verification
        api_key = "d9f88867b0a997ef8e5b91a44b55b8ba2476e00f"

        if any(char.isdigit() for char in username):
            errors["username"] = "username contains character only"

        # Hunter API endpoint
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"

        # Make a request to Hunter API
        response = requests.get(url)

        # Parse the JSON response
        data = response.json()

        # Check if the status is 'valid'
        if data["data"]["status"] != "valid":
            errors["email"] = "email does not exists"

        if User.objects.filter(email=email).exists():
            errors["email"] = "already registered"

        if "@" not in email:
            errors["email"] = "enter valid email address"

        if not len(password) >= 8:
            errors["password"] = "password must be 8 characters"

        if not re.search(r"[!@#$%^&*|<>,(),{}]", password):
            errors["password"] = "password contanis atleast one special character"

        if password != confirm_password:
            errors["conf_password"] = "passwords do not match"

        if errors:
            return render(request, "signup.html", {"errors": errors})
        else:
            User.objects.create_user(username=username, password=password, email=email)

        return redirect("login")
      except:
          return render(request , 'signup.html' ,{'error':'Enter valid data'})

    def get(self, request):
        print("inside get method")
        return render(request, "signup.html")
    
# Login Class
class Login(View):
    def post(self, request):
      try:
        username = request.POST["username"]
        password = request.POST["password"]
    
        user = authenticate(request,username=username,password=password)
        print("value of username and password is:", user.username, user.password)
        if user.check_password(password):
            login(request,user)
            return render(request, "home.html")
        elif not user:
            return render(request, "login.html", {'error':'user does not exists,please register first'})
        else:
            return render(request, "login.html", {"error": "enter valid username or password"})
      except:
          return render(request ,'login.html',{'error':'Enter valid data'})

    def get(self, request):
        print("inside login class")
        return render(request, "login.html")
    
def logout(request):
    auth_logout(request)
    return redirect('login')





# Create your views here.
class HomepageView(TemplateView):
    template_name = "home.html"

# Aboutpage class-based view
class AboutpageView(LoginRequiredMixin,View):
    login_url = 'login/'
    def get(self,request):
        return render(request,'about.html')
    


from django.core.files.storage import FileSystemStorage

class UploadCVView(LoginRequiredMixin,View):
    login_url = 'login/'
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        if 'cv' in request.FILES:
            valid_extensions = ['.jpg', '.png', '.pdf', '.docx'] 
            user = request.user
            file = request.FILES['cv']  # Accessing the uploaded file
            error={}
          # First, check if the file extension is valid
            if not file.name.lower().endswith(tuple(valid_extensions)):
                error['cv'] = "Unsupported file extension. Allowed extensions are: .jpg, .png, .pdf, .docx."
        
            # Check file size (e.g., 5MB limit)
            if file.size > 5 * 1024 * 1024:
                error['cv'] = "File size exceeds the limit of 5 MB."
            
        
          
            if error:
                return render(request,'home.html',{'error':error})
            
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)

            uploaded_file = uploadedfile(file=filename)
            uploaded_file.save()

            
            return HttpResponse("file uploaded succefully")
        
        return render(request, 'home.html', {'error': 'No file uploaded.'})
    
class joblist(LoginRequiredMixin,View):
    login_url = 'login/'
    def get(self,request):
        jobs=Job.objects.all().order_by('-date_posted')
        return render(request,'job_listing.html',{'jobs':jobs})
    
class Post_View(View):
    def get(self, request):
        return render(request, 'blog.html')

    def post(self, request):
        user = request.user
        post_img = request.FILES.get('post_img')
        desc = request.POST.get('desc')  # Safely getting 'desc' to avoid KeyError

        # Ensure both the image and description are provided
        if post_img and desc:
            Post_Info.objects.create(username=user, post_img=post_img, desc=desc)
            return redirect('show_posts')
        else:
            # Handle case where either post_img or desc is missing
            return render(request, 'blog.html', {
                'error': 'Both image and description are required.'
            })


def show_post(request):
    print("ccfc")
    context=Post_Info.objects.all().values()
    print('ALL DATA:',context)
    return render(request,"blog.html",{'context':context})



        # print("inside get method")

        # if qur:
        #     try:
        #         # Filter posts based on the query
        #         context = Post_Info.objects.filter(Q(posted_at=qur) | Q(username__username=qur))
        #         print("Filtering with query:", qur)
        #     except Exception as e:
        #         print(f"Error while filtering posts: {e}")
        #         context = Post_Info.objects.none()  # Return empty queryset on error
        # else:
        #     # Get all posts if no query is provided
        #     context = Post_Info.objects.all()

        # print("Retrieved posts:", context.values())  # Print actual data for debugging

        # # Example: Uncomment and retrieve the liked posts for the current user if needed
        # # if request.user.is_authenticated:
        # #     user_likes = Post_Like.objects.filter(user=request.user).values_list('post_id', flat=True)
        # # else:
        # #     user_likes = []

        # return render(request, 'blog.html', {
        #     'data': context,
        #     # 'user_likes': user_likes,  # Uncomment this if needed in the template
        # })


class contactpage(LoginRequiredMixin,View):
    login_url = 'login/'
    def get(self, request):
        return render(request, 'contact.html')

    
    def post(self, request):
        msg = request.POST.get('message')
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')

        
        if not msg or not name or not email or not subject:
            return HttpResponse("All fields are required", status=400)

      
        data = Contact.objects.create(massege=msg, name=name, email=email, subject=subject)
        
        return HttpResponse("Thank you, your data was successfully submitted.")
    
# class blog(LoginRequiredMixin,View):
#     login_url = 'login/'
#     def get(self,request):
#         return render(request,'blog.html')
    
    

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post_Info, Comment
from .forms import CommentForm

class PostComments(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Display the post details and comments on GET request
        post = get_object_or_404(Post_Info, pk=pk)
        comments = post.comments.all()  # Get all comments related to the post
        comment_form = CommentForm()

        context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        }
        return render(request, 'post_detail.html', context)

    def post(self, request, pk):
        # Handle comment submission on POST request
        post = get_object_or_404(Post_Info, pk=pk)
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post  # Link the comment to the post
            comment.author = request.user  # Set the author to the logged-in user
            comment.save()
            return redirect('post_detail', pk=post.pk)
        
        # If the form is invalid, redisplay the form with errors
        comments = post.comments.all()  # Reload comments to display them again
        context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        }
        return render(request, 'post_detail.html', context)








        