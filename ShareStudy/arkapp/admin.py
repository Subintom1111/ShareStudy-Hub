from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
 
# class CustomUserAdmin(UserAdmin):

#    def get_queryset(self, request):
#        return User.objects.exclude(is_superuser=True)


admin.site.register(User),
admin.site.register(Profile),





