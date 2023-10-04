
from django.urls import path,include
from arkapp import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
urlpatterns = [
    
    path("signup/",views.signup,name="signup"),
    path("signupteach",views.signupteach,name="signupteach"),
    path("",views.index,name="index"),
    
    path("login",views.login,name="login"),
    path("loginhome",views.loginhome,name='loginhome'),
    path("teacherhome/",views.teacherhome,name='teacherhome'),
    path("edit_profile",views.edit_profile,name='edit_profile'),
    path("handlelogout",views.handlelogout,name="handlelogout"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete')
    
]
