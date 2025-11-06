from asyncio import Event
from datetime import datetime

from django.shortcuts import render,redirect
from myapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import CustomUser,Staff,Course,Subject,Session_Year,Staff_Notifications,Staff_Feedback,Staff_leave
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password



# Create your views here.
def index(request):
   return render(request,'index.html')

def hod_home(request):
    staff_count = Staff.objects.count()
    course_count = Course.objects.count()
    subject_count = Subject.objects.count()

    # If gender is stored in Staff model
    male_count = Staff.objects.filter(gender='Male').count()
    female_count = Staff.objects.filter(gender='Female').count()

    context = {
        'staff_count': staff_count,
        'course_count': course_count,
        'subject_count': subject_count,
        'male_count': male_count,
        'female_count': female_count,
    }
    return render(request, 'hod_home.html', context)



def staff_home(request):
    staff = request.user
    notifications = Staff_Notifications.objects.filter(
        staff_id__admin=request.user.id
    ).order_by('-created_at')[:5]

    total_leaves = Staff_leave.objects.filter(staff_id__admin=request.user.id).count()
    unread = Staff_Notifications.objects.filter(staff_id__admin=request.user.id, status=0).count()

    # Example data for chart (replace with actual attendance model if you have one)
    attendance_months = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    attendance_data = [92, 88, 95, 90, 96, 93]

    context = {
        'current_date': datetime.now().strftime("%A, %d %B %Y"),
        'attendance_status': 'Present',
        'total_leaves': total_leaves,
        'unread_notifications': unread,
        'pending_tasks': 2,
        'recent_notifications': notifications,

        'quote_of_the_day': "Excellence is not an act, but a habit.",
        'attendance_months': attendance_months,
        'attendance_data': attendance_data,
    }
    return render(request, 'staff_home.html', context)


def dologin(request):
   if request.method == 'POST':
       # Use Django's `authenticate` function directly
       user = authenticate(
           request,
           username=request.POST.get('email'),
           password=request.POST.get('password')
       )
       if user is not None:
           login(request, user)
           user_type = user.user_type
           if user_type == '1':
               return redirect('hod_home')
           elif user_type == '2':
               return redirect('staff_home')
           elif user_type=='3':
               return redirect('student_home')
           else:


               return redirect('dologin')
       else:
           messages.error(request, 'Invalid Email and Password')
           return redirect('dologin')


   return render(request, 'login.html')

def dashboard(request):
   return render(request,'dashboard.html')

def profile(request):
   user = CustomUser.objects.get(id = request.user.id)
   context = {
       'user':user,
   }
   return render(request,'profile.html')




@login_required(login_url='dologin')
def profile_update(request):
    customuser = get_object_or_404(CustomUser, id=request.user.id)

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.username = username

            if profile_pic:
                customuser.profile_pic = profile_pic

            if password:
                customuser.set_password(password)
                update_session_auth_hash(request, customuser)  # keep logged in

            customuser.save()
            messages.success(request, 'Your profile was successfully updated.')
            return render(request, 'profile.html', {'user': customuser})

        except Exception as e:
            messages.error(request, f'Failed to update your profile: {e}')

    return render(request, 'profile.html', {'user': customuser})

@login_required(login_url='dologin')
def add_staff(request):
   if request.method == 'POST':
       profile_pic = request.FILES.get('profile_pic')
       first_name = request.POST.get('first_name')
       last_name = request.POST.get('last_name')
       email = request.POST.get('email')
       username = request.POST.get('username')
       password = request.POST.get('password')
       address = request.POST.get('address')
       gender = request.POST.get('gender')


       if CustomUser.objects.filter(email=email).exists():
           messages.warning(request, "Email is Already Taken")
           return redirect('add_staff')
       if CustomUser.objects.filter(username=username).exists():
           messages.warning(request, "Username is Already Taken")
           return redirect('add_staff')
       else:
           user = CustomUser(
               first_name=first_name,
               last_name=last_name,
               username=username,
               email=email,
               profile_pic=profile_pic,
               user_type= 2
           )
           user.set_password(password)  # Corrected set_password method
           user.save()
           staff = Staff(
               admin = user,
               address = address,
               gender = gender


           )
           staff.save()
           messages.success(request,"Staff Added Successfully")
           return redirect('add_staff')
   return render(request, 'add_staff.html')


@login_required(login_url='dologin')
def view_staff(request):
   staff = Staff.objects.all()
   context = {
       'staff':staff,
   }
   return render(request,'view_staff.html',context)

@login_required(login_url='dologin')
def edit_staff(request,id):
   staff = Staff.objects.get(id=id)
   context = {
       'staff':staff,
   }
   return render(request,'edit_staff.html',context)

@login_required(login_url='dologin')
def update_staff(request):
   if request.method == 'POST':
       staff_id = request.POST.get('staff_id')
       profile_pic = request.FILES.get('profile_pic')
       first_name = request.POST.get('first_name')
       last_name = request.POST.get('last_name')
       email = request.POST.get('email')
       username = request.POST.get('username')
       password = request.POST.get('password')
       address = request.POST.get('address')
       gender = request.POST.get('gender')


       user = CustomUser.objects.get(id=staff_id)
       user.first_name = first_name
       user.last_name = last_name
       user.email = email
       user.username = username
       if password != None and password != '':
           user.set_password(password)
       if profile_pic != None and profile_pic != '':
           user.profile_pic = profile_pic
       user.save()


       staff = Staff.objects.get(admin = staff_id)
       staff.address = address
       staff.gender = gender
       staff.save()
       messages.success(request,"Staff Updated SuccessFully")
       return redirect('view_staff')
   return render(request,'edit_staff.html')

@login_required(login_url='dologin')
def delete_staff(request,admin):
   staff = CustomUser.objects.get(id=admin)
   staff.delete()
   messages.success(request,'Staff Deleted Successfully')
   return redirect('view_staff')

@login_required(login_url='dologin')
def add_course(request):
   if request.method == 'POST':
       course_name = request.POST.get('course_name')
       course = Course(
           name = course_name,
       )
       course.save()
       messages.success(request,'Course Added Successfully')
       return redirect('add_course')
   return render(request,'add_course.html')

def view_course(request):
   course = Course.objects.all()
   context = {
       'course':course,
   }
   return render(request,'view_course.html',context)


@login_required(login_url='dologin')
def edit_course(request,id):
   course = Course.objects.get(id = id)
   context = {
       'course': course,
   }
   return render(request,'edit_course.html',context)


@login_required(login_url='dologin')
def update_course(request):
   if request.method == 'POST':
       name = request.POST.get('course_name')
       course_id = request.POST.get('course_id')
       course = Course.objects.get(id=course_id)
       course.name = name
       course.save()
       messages.success(request, 'Course Updated Successfully')
       return redirect('view_course')
   return render(request, 'edit_course.html')

@login_required(login_url='dologin')
def delete_course(request,id):
   course = Course.objects.get(id=id)
   course.delete()
   messages.success(request,'Course Deleted Successfully')
   return redirect('view_course')

@login_required(login_url='dologin')
def add_subject(request):
   course = Course.objects.all()
   staff = Staff.objects.all()
   context = {
       'course':course,
       'staff':staff,
   }
   if request.method == 'POST':
       subject_name = request.POST.get('subject_name')
       course_id = request.POST.get('course_id')
       staff_id = request.POST.get('staff_id')


       course = Course.objects.get(id = course_id)
       staff = Staff.objects.get(id = staff_id)


       subject = Subject(
           name = subject_name,
           course = course,
           staff = staff,
       )
       subject.save()
       messages.success(request,"Subject Added SuccessFully")
       return redirect('add_subject')
   return render(request,'add_subject.html',context)

@login_required(login_url='dologin')
def view_subject(request):
   subject = Subject.objects.all()
   context = {
       'subject':subject,
   }
   return render(request,'view_subject.html',context)

@login_required(login_url='dologin')
def edit_subject(request,id):
   subject = Subject.objects.get(id = id)
   course = Course.objects.all()
   staff = Staff.objects.all()
   context = {
       'subject': subject,
       'course':course,
       'staff':staff,
   }
   return render(request, 'edit_subject.html', context)

def update_subject(request):
   if request.method == 'POST':
       subject_id =request.POST.get('subject_id')
       subject_name =request.POST.get('subject_name')
       course_id = request.POST.get('course_id')
       staff_id = request.POST.get('staff_id')




       subject = Subject.objects.get(id=subject_id)
       subject.name = subject_name
       subject.course =Course.objects.get(id=course_id)
       subject.staff =Staff.objects.get(id=staff_id)
       subject.save()


       messages.success(request, "Subject updated successfully!")
       return redirect('view_subject')


   return render(request,'edit_subject.html')

@login_required(login_url='dologin')
def delete_subject(request,id):
   subject = Subject.objects.filter(id=id)
   subject.delete()
   messages.success(request,'Subject Deleted Successfully')
   return redirect('view_subject')

@login_required(login_url='dologin')
def add_session(request):
   if request.method == 'POST':
       session_year_start = request.POST.get('session_year_start')
       session_year_end = request.POST.get('session_year_end')


       session = Session_Year(
           session_start = session_year_start,
           session_end = session_year_end,
       )
       session.save()
       messages.success(request,'Session Added Successfully')
       return redirect('add_session')
   return render(request,'add_session.html')

@login_required(login_url='dologin')
def view_session(request):
   session = Session_Year.objects.all()
   context = {
       'session':session,
   }
   return render(request,'view_session.html',context)

@login_required(login_url='dologin')
def edit_session(request,id):
   session = Session_Year.objects.get(id=id)
   context = {
       'session':session,
   }
   return render(request,'edit_session.html',context)

@login_required(login_url='dologin')
def update_session(request):
   if request.method == 'POST':
       session_id = request.POST.get('session_id')
       session_year_start = request.POST.get('session_year_start')
       session_year_end = request.POST.get('session_year_end')


       session = Session_Year(
           id = session_id,
           session_start = session_year_start,
           session_end = session_year_end,
       )
       session.save()
       messages.success(request,"Session Updated SuccessFully")
       return redirect('view_session')
   return render(request,'edit_session.html')

@login_required(login_url='dologin')
def delete_session(request,id):
   session = Session_Year.objects.get(id=id)
   session.delete()
   messages.success(request,'Session Deleted Successfully')
   return redirect('view_session')


@login_required(login_url='dologin')
def send_staff_notifications(request):
    staff = Staff.objects.all()
    all_notifications = Staff_Notifications.objects.all().order_by('-id')

    context = {
        'staff': staff,
        'all_notifications': all_notifications,
    }
    return render(request, 'send_staff_notifications.html', context)


@login_required(login_url='dologin')
def save_staff_notifications(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        message_text = request.POST.get('message')

        if not staff_id or not message_text:
            messages.error(request, "Please select staff and write a message.")
            return redirect('send_staff_notifications')

        staff = get_object_or_404(Staff, id=staff_id)

        Staff_Notifications.objects.create(
            staff=staff,
            message=message_text
        )

        messages.success(request, "Notification successfully sent")
    return redirect('send_staff_notifications')

def notifications(request):
   staff = Staff.objects.filter(admin = request.user.id)
   for i in staff:
       staff_id = i.id
       notification = Staff_Notifications.objects.filter(staff_id = staff_id)


       context = {
           'notification':notification,
       }
   return render(request,'notifications.html',context)

@login_required(login_url='dologin')
def notifications_done(request,status):
   notification = Staff_Notifications.objects.get(id=status)
   notification.status = 1
   notification.save()
   return redirect('notifications')

@login_required(login_url='dologin')
def staff_feedback(request):
   staff_id = Staff.objects.get(admin=request.user.id)
   feedback_history = Staff_Feedback.objects.filter(staff_id=staff_id)
   context ={
       'feedback_history':feedback_history,
   }
   return render(request,'feedback.html',context)


@login_required(login_url='dologin')
def save_feedback(request):
   if request.method == 'POST':
       feedback = request.POST.get('feedback')
       staff = Staff.objects.get(admin = request.user.id)
       feedback = Staff_Feedback(
           staff_id = staff,
           feedback = feedback,
        )
       feedback.save()
       messages.success(request,'Feedback Sent Successfully')
       return redirect('staff_feedback')
   return render(request, 'feedback.html')

@login_required(login_url='dologin')
def staff_feedback_view(request):
   feedback = Staff_Feedback.objects.all()
   feedback_history = Staff_Feedback.objects.all()
   context = {
       'feedback': feedback,
       'feedback_history':feedback_history,
   }
   return render(request,'staff_feedback.html',context)

@login_required(login_url='dologin')
def staff_feedback_save(request):
   if request.method == 'POST':
       feedback_id = request.POST.get('feedback_id')
       feedback_reply = request.POST.get('feedback_reply')
       feedback = Staff_Feedback.objects.get(id=feedback_id)
       feedback.feedback_reply = feedback_reply
       feedback.status = 1
       feedback.save()
       messages.success(request, 'Feedback Sent Successfully')
   return redirect('staff_feedback_view')

@login_required(login_url='dologin')
def apply_leave(request):
   staff = Staff.objects.filter(admin=request.user.id)
   for i in staff:
       staff_id = i.id
       staff_leave_history = Staff_leave.objects.filter(staff_id=staff_id)
       context = {
           'staff_leave_history': staff_leave_history,
       }
   return render(request, 'apply_leave.html', context)

@login_required(login_url='dologin')
def add_apply_leave(request):
   if request.method == 'POST':
       leave_date = request.POST.get('leave_date')
       leave_message = request.POST.get('leave_message')
       staff = Staff.objects.get(admin=request.user.id)
       leave = Staff_leave(
           staff_id = staff,
           data = leave_date,
           message = leave_message,
       )
       leave.save()
       messages.success(request,'Leave Successfully Sent')
   return redirect('apply_leave')

@login_required(login_url='dologin')
def staff_leave_view(request):
   staff_leave = Staff_leave.objects.all()
   context ={
       'staff_leave':staff_leave,
   }
   return render(request,'staff_leave_view.html',context)

@login_required(login_url='dologin')
def staff_approve_leave(request,id):
   leave = Staff_leave.objects.get(id=id)
   leave.status = 1
   leave.save()
   return redirect('staff_leave_view')

@login_required(login_url='dologin')
def staff_disapprove_leave(request,id):
   leave = Staff_leave.objects.get(id=id)
   leave.status = 2
   leave.save()
   return redirect('staff_leave_view')

def dologout(request):
   logout(request)
   return redirect('dologin')

def student_page(request):
   return render(request,'student_page.html')

User = get_user_model()
def student_register(request):
   if request.method == 'POST':
       first_name = request.POST.get('first_name')
       last_name = request.POST.get('last_name')
       email = request.POST.get('email')
       password = request.POST.get('password')
       confirm_password = request.POST.get('confirm_password')
       profile_pic = request.FILES.get('profile_pic')


       # Validation
       if password != confirm_password:
           messages.error(request, 'Passwords do not match!')
           return redirect('student_register')


       if User.objects.filter(email=email).exists():
           messages.error(request, 'Email already exists!')
           return redirect('student_register')


       # Create user
       user = User(
           first_name=first_name,
           last_name=last_name,
           username=email,
           email=email,
           user_type='3',  # student
           profile_pic=profile_pic
       )
       user.password = make_password(password)
       user.save()


       messages.success(request, 'Student registered successfully! You can now log in.')
       return redirect('dologin')


   return render(request, 'student_register.html')


def student_home(request):
    courses = Course.objects.all()
    staffs = Staff.objects.all()
    subjects = Subject.objects.all()

    context = {
        "courses": courses,
        "staffs": staffs,
        "subjects": subjects
    }

    return render(request, "student_home.html", context)
