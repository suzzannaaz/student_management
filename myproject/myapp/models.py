from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
   USER = (
       (1, 'HOD'),
       (2, 'STAFF'),
       (3, 'STUDENT')
      )


   user_type = models.CharField(choices=USER, max_length=50, default=1)
   profile_pic = models.ImageField(upload_to='media/profile_pic')

class Staff(models.Model):
   admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
   address = models.TextField(max_length=100)
   gender = models.CharField(max_length=100)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)


   def __str__(self):
       return self.admin.username

class Course(models.Model):
   name = models.CharField(max_length=100)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)


   def __str__(self):
       return self.name

class Subject(models.Model):
   name = models.CharField(max_length=100)
   course = models.ForeignKey(Course,on_delete=models.CASCADE)
   staff = models.ForeignKey(Staff,on_delete=models.CASCADE)


   def __str__(self):
       return self.name

class Session_Year(models.Model):
   session_start = models.DateField()
   session_end = models.DateField()


   def __str__(self):
       return f"{self.session_start} To {self.session_end}"

class Staff_Notifications(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"{self.staff.admin.first_name} - {self.message[:20]}"

class Staff_Feedback(models.Model):
   staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
   feedback = models.TextField()
   feedback_reply = models.TextField(blank=True, null=True)  # Allow blank replies
   status = models.IntegerField(default=0)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now_add=True)


   def __str__(self):
       return self.staff_id.admin.first_name + self.staff_id.admin.last_name

class Staff_leave(models.Model):
   staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
   data = models.CharField(max_length=100)
   message = models.TextField()
   status = models.IntegerField(default=0)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now_add=True)


   def __str__(self):
       return self.staff_id.admin.first_name + self.staff_id.admin.last_name
