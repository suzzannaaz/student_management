from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Staff)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Session_Year)
admin.site.register(Staff_Notifications)
admin.site.register(Staff_Feedback)
admin.site.register(Staff_leave)


