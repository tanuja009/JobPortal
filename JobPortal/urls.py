"""
URL configuration for JobPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from JobPortalApp import views
from django.conf import settings
from django.conf.urls.static import static
from JobPortalApp.views import HomepageView, AboutpageView,UploadCVView,SignUp,Login,joblist,contactpage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomepageView.as_view(), name='home'),
    path('about/', AboutpageView.as_view(), name='about'),
    path('uploadcv/',UploadCVView.as_view(),name="upload_cv"),
    path('signup/',SignUp.as_view(),name="SignUp"),
    path('login/',Login.as_view(),name="login"),
    path("accounts/", include("allauth.urls")),
    path("joblist/",joblist.as_view(),name="joblist"),
    path('logout/',views.logout,name="logout"),
    path('contactpage/', contactpage.as_view(), name='contactpage'),
    # path('blog/',blog.as_view(),name="blog"),
    path('show_post/',views.show_post,name="show_post")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
