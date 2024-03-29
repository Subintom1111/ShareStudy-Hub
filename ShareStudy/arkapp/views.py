from django.shortcuts import render,redirect,HttpResponse
from .models import User 
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.cache import never_cache

from django.contrib.auth import authenticate ,login as auth_login,logout,get_user_model
from django.contrib import messages
from django.views.generic import View
from .models import Profile
from .models import Profilete


from django.db.models import Q
#activate
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login,logout
from django.utils.encoding import DjangoUnicodeDecodeError
import re
from django.contrib.auth.decorators import login_required
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
               
               return redirect('adminnew')
                          
        else:
            messages.error(request,"Some thing went wrong")
            return redirect('login')
    response = render(request,'login.html')
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response



def signupteach(request):
            
   return render(request,'signupteach.html')



@never_cache
@login_required(login_url="login")
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
@never_cache
@login_required(login_url="login")
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
@never_cache
@login_required(login_url="login")
def edit_profilete(request):
    if request.method == 'POST':
        # Process the form data and update the user's profile
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        email = request.POST.get('email','')
       
        if User.objects.filter(username=email).exclude(id=request.user.id).exists():
            messages.warning(request, "Email is already taken")
            return redirect('edit_profilete')  # Redirect to the same page with the warning message

        
        
        
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
       


@never_cache
@login_required(login_url="login")
def adminnew(request):
    return render(request,'adminnew.html')




def userview(request):
    role_filter = request.GET.get('role')
    users = User.objects.filter(~Q(is_superuser=True))  # Exclude superusers by default

    if role_filter:
        users = users.filter(role=role_filter)

    context = {'User_profiles': users, 'role_filter': role_filter}
    return render(request,'userview.html',context)






def teacherview(request):
     return render(request,'teacherview.html')


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags





  
def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    subject = 'Account Activation'
    html_message = render_to_string('activation_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'prxnv2832@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return redirect('userview')

def deactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_superuser:
        return HttpResponse("You cannot deactivate the admin.")
    user.is_active = False
    user.save()
    subject = 'Account Deactivation'
    html_message = render_to_string('deactivation_email.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'prxnv2832@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    # Send an email to the user here
    return redirect('userview')

#################################################################################

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Courses

def add_course(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        description = request.POST.get("description")
        assigned_teacher_id = request.POST.get("assigned_teacher")
        credit_hours = request.POST.get("credit_hours")
        course_fee = request.POST.get("course_fee")
        available_seats = request.POST.get("available_seats")

        if course_name and assigned_teacher_id and credit_hours and course_fee and available_seats:
            try:
                assigned_teachers= get_object_or_404(User, id=assigned_teacher_id)
            except User.DoesNotExist:
                return HttpResponse("Selected teacher does not exist.", status=400)

            # Create a new course object and save it to the database
            course = Courses(
                course_name=course_name,
                description=description,
                assigned_teachers=assigned_teachers.username,  # Assuming you want to store the username of the teacher
                credit_hours=credit_hours,
                course_fee=course_fee,
                available_seats=available_seats
            )
            course.save()

            # Redirect to a success page or any other appropriate URL
            return redirect('add_course')  # Replace 'add_course' with your desired URL name
        else:
            return HttpResponse("Invalid form data.", status=400)

    # Fetch a list of teachers from the User model with the 'TEACHER' role
    teachers = User.objects.filter(role='TEACHER')  # Adjust 'role' and 'User' as per your user model

    return render(request, 'add_course.html', {'teachers': teachers})


###################################################################################

def exammarkset(request):
     return render(request,'exammarkset.html')


def examdetails(request):
     return render(request,'examdetails.html')



##########################################################################


def view_course(request):
    courses = Courses.objects.all()  # Retrieve all courses
    return render(request, 'view_course.html', {'courses': courses})




def delete_course(request, course_id):
    try:
        course = Courses.objects.get(id=course_id)
        course.delete()
    except Courses.DoesNotExist:
        
        pass 

    return redirect('view_course')  


#################################################################################


from django.shortcuts import render, redirect
from .models import Feedback
from django.contrib.auth.decorators import login_required

@never_cache
@login_required(login_url="login")
def submit_feedback(request):
    if request.method == "POST":
        feedback_message = request.POST.get('feedback_message')
        if feedback_message:
            Feedback.objects.create(student=request.user, message=feedback_message)
            # You can add additional logic here (e.g., sending a confirmation email)
            return redirect('feedback_thankyou')

    return render(request, 'feedback_form.html')


def feedback_thankyou(request):
     return render(request,'feedback_thankyou.html')


from django.shortcuts import render
from .models import Feedback

def adminfeedback(request):
    feedback_list = Feedback.objects.all()
    return render(request, 'adminfeedback.html', {'feedback_list': feedback_list})


#######################################################################################


from django.shortcuts import render, redirect
from .models import ExamMark

def exammarkset(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        question_number = request.POST.get('question_number')
        total_marks = request.POST.get('total_marks')
        exam_time = request.POST.get('exam_time')
        
        print(f"course_name: {course_name}")
        print(f"question_number: {question_number}")
        print(f"total_marks: {total_marks}")
        print(f"exam_time: {exam_time}")

        if course_name and question_number and total_marks and exam_time:
            exam = ExamMark(
                course_name=course_name,
                question_number=question_number,
                total_marks=total_marks,
                exam_time=exam_time
            )
            exam.save()
            print("Data saved to the database")
        else:
            print("Some fields are missing")
    return render(request, 'exammarkset.html')

#####################################################################################


from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment,Submission

@never_cache
@login_required(login_url="login")
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignment_list.html', {'assignments': assignments})

def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, 'assignment_detail.html', {'assignment': assignment,'submissions':submissions})

def create_assignment(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        teacher = request.user  # Assign the current teacher as the creator

        Assignment.objects.create(
            title=title,
            description=description,
            deadline=deadline,
            teacher=teacher,
        )

        return redirect('assignment_list')

    return render(request, 'create_assignment.html')

def update_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')

        assignment.title = title
        assignment.description = description
        assignment.deadline = deadline
        assignment.save()

        return redirect('assignment_list')

    return render(request, 'update_assignment.html', {'assignment': assignment})

def delete_assignment(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)
    assignment.delete()
    return redirect('assignment_list')


@never_cache
@login_required(login_url="login")
def assignstu_list(request):
    
    assignments = Assignment.objects.all()
    return render(request, 'assignstu_list.html', {'assignments': assignments})




from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment, Submission

def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']

        # Create a new submission
        submission = Submission.objects.create(
            student=request.user,
            assignment=assignment,
            document=uploaded_file
        )
        
        # Save the submission to the database
        submission.save()

        # Redirect to a different view (e.g., student_assignment_list)
        return redirect('assignstu_list')  # Replace with the correct view name

    return render(request, 'submit_assignment.html', {'assignment': assignment})




def view_student_names(request, assignment_id):
    submissions = Submission.objects.filter(assignment_id=assignment_id)
    # You can pass the list of students to the template
    students = [submission.student for submission in submissions]

    return render(request, 'view_student_names.html', {'students': students})


def list_submissions(request):
    # Implement a view for teachers to list submissions
    submissions = Submission.objects.all()
    return render(request, 'list_submissions.html', {'submissions': submissions})

def download_assignment(request, submission_id):
    # Implement a view for teachers to download assignments
    submission = get_object_or_404(Submission, id=submission_id)
    # Implement code to serve the file for download
    response = HttpResponse(submission.document, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{submission.document.name}"'
    return response


################################################################################################



def stu_sidecourse(request, course_id):
    # Retrieve the course details based on the course_id
    course = get_object_or_404(Courses, id=course_id)
    
    # Render the template with the course details
    return render(request, 'stu_sidecourse.html', {'course': course})


############################################################################################


from .models import Notification
def send_notification(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        users = User.objects.all()

        # Create a notification for each user
        for user in users:
            Notification.objects.create(user=user, message=message)

        return redirect('send_notification')  # Redirect to admin dashboard or any desired page

    return render(request, 'send_notification.html')


def view_notifications(request):
    # Retrieve notifications for the logged-in student
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')

    # Mark notifications as read
    notifications.update(is_read=True)

    return render(request, 'view_notifications.html', {'notifications': notifications})

def admin_notifications(request):
    
        notifications = Notification.objects.all().order_by('-timestamp')

        if request.method == 'POST':
            # Handle notification deletion
            notification_id = request.POST.get('delete_notification')
            if notification_id:
                Notification.objects.filter(id=notification_id).delete()
                return redirect('admin_notifications')

        return render(request, 'admin_notifications.html', {'notifications': notifications})

#######################################################################################################

from .models import CourseNotes, User

def upload_course_notes(request):
    if request.method == 'POST':
    
        title = request.POST['title']
        description = request.POST['description']
        pdf_file = request.FILES['pdf_file']
        
        # Assuming you have a User model with a 'username' field
        # You may need to adjust this depending on your actual models
        
        
        course_notes = CourseNotes( title=title, description=description, pdf_file=pdf_file)
        course_notes.save()
    return render(request, 'upload_course_notes.html')

def download_course_notes(request, notes_id):
    course_notes = get_object_or_404(CourseNotes, pk=notes_id)
    file_path = course_notes.pdf_file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{course_notes.pdf_file.name}"'
        return response

def view_course_notes(request):
    course_notes = CourseNotes.objects.all()
    return render(request, 'view_course_notes.html', {'course_notes': course_notes})

