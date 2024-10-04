from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class HomepageView(TemplateView):
    template_name = "home.html"

# Aboutpage class-based view
class AboutpageView(View):
    def get(self,request):
        return render(request,'about.html')
    


from django.core.files.storage import FileSystemStorage

class UploadCVView(LoginRequiredMixin,View):
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
    
class Job_Listing(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'job_listing.html')
    def post(self,request):
        pass

        