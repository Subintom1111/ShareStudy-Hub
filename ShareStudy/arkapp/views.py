from django.shortcuts import render,redirect,HttpResponse
from .models import User 
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.cache import never_cache

from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib import messages
from django.views.generic import View

#Student Home Page
def loginhome(request):
    if 'username' in request.session:
        response = render(request,'loginhome.html')
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')
    
@never_cache
def index(request):

    return render(request,'index.html')



# Create your views here.

#Signup Page For Students
def signup(request):
   if request.method=="POST":
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            email=request.POST['email']
            username=request.POST['username']
            password=request.POST['password']
            confirm_password=request.POST['confirm_password']
            if password!=confirm_password:
                    messages.warning(request,"password is not matching")
                    return render(request,'signup.html')
            try:
                      if User.objects.get(username=username):
                             messages.warning(request,"Username is already taken")
                             return render(request,'signup.html')
            except Exception as identifiers:
                      pass
            print(first_name,last_name,username,email,password)
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password,role='STUDENT')
              #make the user inactive  user.is_active=False
            user.save()
            
            return redirect('login')
   return render(request,'signup.html')
            
   #Login Page  
def login(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        
        # Use the model class to query the database
        user = authenticate(request,username=username, password=password)
        
        if user is not None:
            auth_login(request,user)
            request.session['username']=username
            if user.role=='STUDENT':
              # messages.success(request,"Login Success!!!")
               return redirect('loginhome')
            elif user.role=='TEACHER':
               messages.success(request,"Login Success!!!")
               return HttpResponse("seller login")
            elif user.role=='ADMIN':
               messages.success(request,"Login Success!!!")
               return HttpResponse("Admin login ")
                          
        else:
            messages.error(request,"Some thing went wrong")
            return redirect('login')
    response = render(request,'login.html')
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response

def signupteach(request):
            
   return render(request,'signupteach.html')



def teacherhome(request):
     return render(request,'teacherhome.html')



def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def edit_profile(request):
     return render(request,'edit_profile.html')

     

    