
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
]
