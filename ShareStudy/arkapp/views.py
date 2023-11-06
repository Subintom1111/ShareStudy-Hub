from django.shortcuts import render,redirect,HttpResponse
from .models import User 
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.cache import never_cache

from django.contrib.auth import authenticate ,login as auth_login,logout,get_user_model
from django.contrib import messages
from django.views.generic import View
from .models import Profile
from .models import Profilete


#activate
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login,logout
from django.utils.encoding import DjangoUnicodeDecodeError
import re

from django.views.generic import View
#from .utils import *

#for activating user account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from .utils import TokenGenerator,generate_token

# Create your views here.

#email
from django.conf import settings
from django.core.mail import EmailMessage

#threading
import threading

class EmailThread(threading.Thread):
       def __init__(self, email_message):
              super().__init__()
              self.email_message=email_message
       def run(self):
              self.email_message.send()

#reset passwor generater
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.auth import authenticate, login, get_user_model


#Student Home Page
def loginhome(request):
    if 'email' in request.session:
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
            username=email
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
              #make the user inactive  
            user.is_active=False
            user.save()

            #authenticate
            current_site=get_current_site(request)  
            email_subject="Activate your account"
            message=render_to_string('activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()

            messages.info(request,"Activate Your Account by Clicking Link on your Email")

            return redirect('login')
   return render(request,'signup.html')
            


def signupteacher(request):
   if request.method=="POST":
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            email=request.POST['email']
            username=email
            password=request.POST['password']
            confirm_password=request.POST['confirm_password']
            
            if password!=confirm_password:
                    messages.warning(request,"password is not matching")
                    return render(request,'signupteacher.html')
            try:
                      if User.objects.get(username=username):
                             messages.warning(request,"Username is already taken")
                             return render(request,'signupteacher.html')
            except Exception as identifiers:
                      pass
            print(first_name,last_name,username,email,password)
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password,role='TEACHER')
              #make the user inactive  
            user.is_active=False
            user.save()

            #authenticate
            current_site=get_current_site(request)  
            email_subject="Activate your account"
            message=render_to_string('activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()

            messages.info(request,"Activate Your Account by Clicking Link on your Email")

            return redirect('login')
   return render(request,'signupteacher.html')

   #Login Page  
def login(request):
    
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email, password)
        
        # Use the model class to query the database
        user = authenticate(request,username=email, password=password)
        
        if user is not None:
            auth_login(request,user)
            request.session['email']=email
            if user.role=='STUDENT':
              # messages.success(request,"Login Success!!!")
               return redirect('loginhome')
            elif user.role=='TEACHER':
               messages.success(request,"Login Success!!!")
               return redirect('teacherhome')
            elif user.role=='ADMIN':
               
               return redirect('custom_admin_page')
                          
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

     

def adminreg(request):
    # Query all User objects (using the custom user model) from the database
    User = get_user_model()
    user_profiles = User.objects.all()
    
    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    
    # Render the HTML template
    return render(request, 'admin.html', context)




class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account activated sucessfully")
            return redirect('login')
        return render(request,"activatefail.html")
    

#student
def edit_profile(request):
    if request.method == 'POST':
        # Process the form data and update the user's profile
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        email = request.POST.get('email','')
        contact = request.POST.get('contact','')
        course = request.POST.get('course','')
        gender = request.POST.get('gender','')
        if User.objects.filter(username=email).exclude(id=request.user.id).exists():
            messages.warning(request, "Email is already taken")
            return redirect('edit_profile')  # Redirect to the same page with the warning message

        # Validate phone
        if Profile.objects.filter(contact=contact).exclude(user=request.user).exists():
            messages.warning(request, "Phone number is already taken")
            return redirect('edit_profile')  # Redirect to the same page with the warning message

        # Validate course
        if Profile.objects.filter(course=course).exclude(user=request.user).exists():
            return redirect('edit_profile')
        
        # Validate gender
        if Profile.objects.filter(gender=gender).exclude(user=request.user).exists():
            return redirect('edit_profile')
        
        
        if email != request.user.email:
            user=request.user
            user.email=email
            user.username=email
            user.is_active=False  #make the user inactive
            user.save()
            
            
            current_site=get_current_site(request)  
            email_subject="Activate your account"
            message=render_to_string('activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()
            messages.info(request,"Active your account by clicking the link send to your email")
            logout(request)
           
            return redirect('login')
            
        
        # Update the User model fields
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username=email
        user.email = email
        user.save()
        
        # Update the Profile model fields
        profile, created = Profile.objects.get_or_create(user=user)
        profile.contact = contact
        profile.course = course
        profile.gender = gender
        profile.save()
        
        # Logout the user and redirect to the signup page
        messages.success(request,'profile updated')
        return redirect('edit_profile')
    else:
        return render(request, 'edit_profile.html', {'user': request.user})
      


#teacher
def edit_profilete(request):
    if request.method == 'POST':
        # Process the form data and update the user's profile
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        email = request.POST.get('email','')
        contact = request.POST.get('contact','')
        course = request.POST.get('course','')
        gender = request.POST.get('gender','')
        if User.objects.filter(username=email).exclude(id=request.user.id).exists():
            messages.warning(request, "Email is already taken")
            return redirect('edit_profilete')  # Redirect to the same page with the warning message

        # Validate phone
        if Profilete.objects.filter(contact=contact).exclude(user=request.user).exists():
            messages.warning(request, "Phone number is already taken")
            return redirect('edit_profilete')  # Redirect to the same page with the warning message

        # Validate course
        if Profilete.objects.filter(course=course).exclude(user=request.user).exists():
            return redirect('edit_profilete')
        
        # Validate gender
        if Profilete.objects.filter(gender=gender).exclude(user=request.user).exists():
            return redirect('edit_profilete')
        
        
        if email != request.user.email:
            user=request.user
            user.email=email
            user.username=email
            user.is_active=False  #make the user inactive
            user.save()
            
            
            current_site=get_current_site(request)  
            email_subject="Activate your account"
            message=render_to_string('activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()
            messages.info(request,"Active your account by clicking the link send to your email")
            logout(request)
           
            return redirect('login')
            
        
        # Update the User model fields
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username=email
        user.email = email
        user.save()
        
        # Update the Profile model fields
        profilete, created = Profilete.objects.get_or_create(user=user)
        profilete.contact = contact
        profilete.course = course
        profilete.gender = gender
        profilete.save()
        
        # Logout the user and redirect to the signup page
        messages.success(request,'profile updated')
        return redirect('edit_profilete')
    else:
        return render(request, 'edit_profilete.html', {'user': request.user})
      


#for admin
def custom_admin_page(request):
     User = get_user_model()
     user_profiles = User.objects.all()
     context = {'user_profiles': user_profiles}
     return render(request, 'admin.html', context)
       





from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import User
from django.template.loader import render_to_string
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
         # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'prxnv2832@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been deactivated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already deactivated.")
    return redirect('custom_admin_page')

def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
        subject = 'Account activated'
        message = 'Your account has been activated.'
        from_email = 'prxnv2832@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect('custom_admin_page')