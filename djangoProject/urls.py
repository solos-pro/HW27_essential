"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from advertisement.views import AdDetailView, AdsView, CatView, CatDetailView, InitDB
# from advertisement import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('cat/', CatView.as_view()),
    path ('add/', InitDB.as_view()),
    path ('cat/<int:pk>', CatDetailView.as_view()),
    path ('ad/', AdsView.as_view()),
    path ('ad/<int:pk>', AdDetailView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
