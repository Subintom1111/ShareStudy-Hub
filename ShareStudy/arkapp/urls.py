
from django.urls import path,include
from arkapp import views
urlpatterns = [
    
    path("signup/",views.signup,name="signup"),
    path("signupteach/",views.signupteach,name="signupteach"),
    path("",views.index,name="index"),
    
    path("login",views.login,name="login"),
    path("loginhome",views.loginhome,name='loginhome'),
    path("teacherhome/",views.teacherhome,name='teacherhome'),
    path("studenthome/",views.studenthome,name='studenthome'),
   
    
]
