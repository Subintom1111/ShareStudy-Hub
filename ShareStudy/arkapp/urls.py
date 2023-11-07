
from django.urls import path,include
from arkapp import views
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
urlpatterns = [
    
    path("signup/",views.signup,name="signup"),
    path("signupteacher/",views.signupteacher,name="signupteacher"),
    path("",views.index,name="index"),
    path("login",views.login,name="login"),
    path("adminreg",views.adminreg,name="adminreg"),
    path("loginhome",views.loginhome,name='loginhome'),
    path("teacherhome/",views.teacherhome,name='teacherhome'),
    path("edit_profile",views.edit_profile,name='edit_profile'),
    path("edit_profilete/",views.edit_profilete,name='edit_profilete'),
    path("handlelogout",views.handlelogout,name="handlelogout"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),   
    path('custom_admin_page/', views.custom_admin_page, name='custom_admin_page'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path("adminnew",views.adminnew,name='adminnew'),
    path("userview",views.userview,name='userview'),
    path("teacherview",views.teacherview,name='teacherview'),
    path("add_course",views.add_course,name='add_course'),
    path("exammarkset",views.exammarkset,name='exammarkset'),
    path("view_course",views.view_course,name='view_course'),
    path("examdetails",views.examdetails,name='examdetails'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('feedback_thankyou/', views.feedback_thankyou, name='feedback_thankyou'), 
    path("adminfeedback",views.adminfeedback,name='adminfeedback'),
    path('exammarkset/', views.exammarkset, name='exammarkset'),
    path('assignment_list', views.assignment_list, name='assignment_list'),
    path('<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('create/', views.create_assignment, name='create_assignment'),
    path('update/<int:assignment_id>/', views.update_assignment, name='update_assignment'),
    path('delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('assignstu_list', views.assignstu_list, name='assignstu_list'),
    path('submit_assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('view_student_names/<int:assignment_id>/', views.view_student_names, name='view_student_names'),


    
]
