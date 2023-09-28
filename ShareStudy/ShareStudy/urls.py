
from django.contrib import admin
from django.urls import path,include
from arkapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('arkapp.urls')),
    
]
