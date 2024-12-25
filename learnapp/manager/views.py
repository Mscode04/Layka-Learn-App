from datetime import datetime
from django.http import JsonResponse
from .models import CourseEnrollment, Rating,UserProfile, LoginTable, MentorProfile
from django.shortcuts import get_object_or_404, render, redirect
from .forms import MentorProfileForm, SelectStudentCourseForm
from .models import Course, CourseFile
from django.contrib import messages
from django.conf import settings
from .forms import CheckoutForm
from django.urls import reverse
from .forms import CourseForm
from .forms import RatingForm
from .models import Payment
from .models import Course
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def UserRegistration(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        password1 = request.POST['password1']
        country = request.POST.get('country', '')
        state = request.POST.get('state', '')
        if password != password1:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        userprofile = UserProfile(
            name=name,
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            password1=password,  
            country=country,
            state=state,
        )
        userprofile.save()
        messages.success(request, 'Registration completed!')
        return redirect('login')
    return render(request, 'manager/register.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_details = LoginTable.objects.get(username=username)
            if password == user_details.password:
                request.session['username'] = user_details.username
                if user_details.type == 'user':
                    return redirect('user_view')
                elif user_details.type == 'manager':
                    return redirect('admin_view')
                elif user_details.type == 'mentor':
                    return redirect('mentor_view')
            else:
                messages.error(request, 'Invalid username or password.')
        except LoginTable.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'manager/login.html')


def adminView(request):
    user_name = request.session.get('username')
    return render(request, 'manager/manager-dashbord.html', {'user_name': user_name})


def userView(request):
    user_name = request.session.get('username')
    return render(request, 'student/student-dashbord.html', {'user_name': user_name})

def mentorView(request):
    user_name = request.session.get('username')
    return render(request, 'mentor/mentor-dashbord.html', {'user_name': user_name})

def Logout(request):
    request.session.flush()
    return redirect('login')

def user_details(request):
    users = UserProfile.objects.all()
    return render(request, 'manager/userdetails.html', {'users': users})


def mentor_list(request):
    mentors = LoginTable.objects.filter(type='mentor')
    mentor_profiles = MentorProfile.objects.filter(mentor__in=mentors)  
    return render(request, 'manager/mentor_list.html', {'mentor_profiles': mentor_profiles})


def add_mentor(request):
    if request.method == 'POST':
        form = MentorProfileForm(request.POST, request.FILES)
        if form.is_valid():
            mentor_profile = form.save(commit=False)
            login_user = LoginTable.objects.get(id=request.POST.get('mentor'))  
            mentor_profile.mentor = login_user
            mentor_profile.save()
            return redirect('mentor_list')  
    else:
        form = MentorProfileForm()
    return render(request, 'manager/add_mentor.html', {'form': form})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            additional_files = request.FILES.getlist('additional_parts') 
            for file in additional_files:
                course_file = CourseFile(file=file)
                course_file.save()
                course.additional_parts.add(course_file) 
            course.save()  
            return redirect('course_list')  
    else:
        form = CourseForm()
    return render(request, 'manager/add-cource.html', {'form': form})


def update_course(request, id):
    course = get_object_or_404(Course, id=id)
    form = CourseForm(request.POST or None, request.FILES or None, instance=course)
    if request.method == 'POST':
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            additional_files = request.FILES.getlist('additional_parts')  
            for file in additional_files:
                course_file = CourseFile(file=file)
                course_file.save()
                course.additional_parts.add(course_file)
            course.save()
            return redirect('course_list')  
    return render(request, 'manager/update-course.html', {'form': form, 'course': course})

def course_list(request):
    courses = Course.objects.all() 
    return render(request, 'manager/course_list.html', {'courses': courses})


def course_list_std(request):
    courses = Course.objects.all() 
    return render(request, 'student/course_list_std.html', {'courses': courses})


def allocate_mentor(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    mentors = MentorProfile.objects.all()

    if request.method == 'POST':
        mentor_id = request.POST.get('mentor')
        if mentor_id:
            mentor = get_object_or_404(MentorProfile, id=mentor_id)
            user.mentor = mentor
            user.save()
            return redirect('user_details')  
    return render(request, 'manager/allocate_mentor.html', {'user': user, 'mentors': mentors})


def create_checkout_session(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            payment = Payment.objects.create(
                course=course,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                amount_paid=course.price,
            )
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': course.course_name,
                            },
                            'unit_amount': int(course.price * 100),  
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')) + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri(reverse('cancel')),
            )
            payment.session_id = checkout_session.id
            payment.save()
            return redirect(checkout_session.url, code=303)
    else:
        form = CheckoutForm()
    return render(request, 'student/checkout.html', {'form': form, 'course': course})


def success(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    payment = Payment.objects.get(session_id=session_id)
    if session.payment_status == 'paid':
        payment.payment_status = 'paid'
    else:
        payment.payment_status = 'failed'
    payment.save()
    return render(request, 'student/success.html', {'payment': payment})

def cancel(request):
    return render(request, 'student/cancel.html')

def purchase_students(request):
    payments = Payment.objects.all()
    return render(request, 'manager/purchase_students.html', {'payments': payments})


def mentor_list_std(request):
    mentors = LoginTable.objects.filter(type='mentor', username='mentor2')
    mentor_profiles = MentorProfile.objects.filter(mentor__in=mentors)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            mentor_name = request.POST.get('mentor_name')
            mentor_profile = MentorProfile.objects.get(mentor__username=mentor_name)  
            rating = form.save(commit=False)
            rating.mentor = mentor_profile
            rating.save()
            return redirect('mentor_list_std')  
    else:
        form = RatingForm()
    return render(request, 'student/student-mentor.html', {
        'mentor_profiles': mentor_profiles,
        'form': form,
    })
    
    
# def rating_page(request):
#     ratings = Rating.objects.all()
#     return render(request, 'manager/rating-page-mentor.html', {'ratings': ratings})    



def rating_page(request):
    ratings = Rating.objects.all()

    # Process the ratings to split the student name if it contains the specified keywords
    for rating in ratings:
        student_name = rating.student_name.lower()  # Convert to lowercase for case-insensitive comparison
        
        if 'digital marketing' in student_name:
            name_parts = rating.student_name.split('digital marketing')
            rating.student_name = {'before_keyword': name_parts[0], 'keyword': 'digital marketing'}
        elif 'python full stack' in student_name:
            name_parts = rating.student_name.split('python full stack')
            rating.student_name = {'before_keyword': name_parts[0], 'keyword': 'python full stack'}
        else:
            rating.student_name = {'before_keyword': rating.student_name, 'keyword': ''}

    return render(request, 'manager/rating-page-mentor.html', {'ratings': ratings})


def enrollment_page(request):
    enrollments = CourseEnrollment.objects.all()
    return render(request, 'manager/enrollment-page.html', {'enrollments': enrollments})

def select_student_course(request):
    if request.method == 'POST':
        form = SelectStudentCourseForm(request.POST)
        if form.is_valid():
            student_details = form.cleaned_data['student']
            course_details = form.cleaned_data['course']

            try:
                course_enrollment = CourseEnrollment(
                    student=student_details,
                    course=course_details,
                    student_name=student_details.name,  
                    course_name=course_details.course_name  
                )
                course_enrollment.save()
                return redirect('course_success')  
            except Exception as e:
                error_message = f"An unexpected error occurred: {e}"
                return render(request, 'manager/select-student-course.html', {
                    'form': form,
                    'error_message': error_message,
                })
    else:
        form = SelectStudentCourseForm()
    return render(request, 'manager/select-student-course.html', {'form': form})


def suc_course(request):
    return render(request,'manager/course-success.html')



# def mycourse_list_std(request):
#     payment_course_names = Payment.objects.values_list('course__course_name', flat=True).distinct()
#     courses = Course.objects.filter(course_name__in=payment_course_names)
#     return render(request, 'student/my-course.html', {'courses': courses})


# def mycourse_list_std(request):
#     # Fetch distinct course names from Payment model
#     payment_course_names = Payment.objects.values_list('course__course_name', flat=True).distinct()
    
#     # Fetch courses that match those course names from the Course model
#     courses = Course.objects.filter(course_name__in=payment_course_names)
    
#     return render(request, 'student/my-course.html', {'courses': courses})

def mycourse_list_std(request):
    # Fetch distinct course names from the Payment model
    payment_course_names = Payment.objects.values_list('course__course_name', flat=True).distinct()
    
    # Fetch courses that match those course names from the Course model
    courses = Course.objects.filter(course_name__in=payment_course_names)

    # Handle form submission for rating
    if request.method == "POST":
        course_name = request.POST.get("course_name")  # Optional course_name
        student_name = request.POST.get("student_name")
        rating = request.POST.get("rating")

        # Get the mentor based on the course
        mentor = None
        if course_name:
            try:
                course = Course.objects.get(course_name=course_name)
                mentor = course.mentor
            except Course.DoesNotExist:
                pass  # Handle the case if the course is not found

        # Create the rating entry
        if student_name and rating and mentor:
            Rating.objects.create(
                mentor=mentor,
                student_name=student_name,
                rating=int(rating)
            )

        # Redirect back to the same page after submission
        return redirect('mycourse_list_std')  # Adjust the URL if needed

    return render(request, 'student/my-course.html', {'courses': courses})











def student_progress(request):
    # Sample course data (this would normally come from your database)
    courses = [
        {'course_name': 'Course 1', 'student_name': 'John Doe', 'progress': 40},
       
    ]
    return render(request, 'student/progress.html', {'courses': courses})

def student_progress_admin(request):
    # Sample course data (this would normally come from your database)
    courses = [
        {'course_name': 'Course 1', 'student_name': 'John Doe', 'progress': 40},
       
    ]
    return render(request, 'student/progress.html', {'courses': courses})

def student_progress_mentor(request):
    # Sample course data (this would normally come from your database)
    courses = [
        {'course_name': 'Course 1', 'student_name': 'John Doe', 'progress': 40},
       
    ]
    return render(request, 'mentor/progress.html', {'courses': courses})





def update_course_mentor(request, id):
    course = get_object_or_404(Course, id=id)
    form = CourseForm(request.POST or None, request.FILES or None, instance=course)
    if request.method == 'POST':
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            additional_files = request.FILES.getlist('additional_parts')  
            for file in additional_files:
                course_file = CourseFile(file=file)
                course_file.save()
                course.additional_parts.add(course_file)
            course.save()
            return redirect('course_list')  
    return render(request, 'mentor/update-course.html', {'form': form, 'course': course})

def course_list_mentor(request):
    courses = Course.objects.all() 
    return render(request, 'mentor/course_list.html', {'courses': courses})


def user_details_mentor(request):
    users = UserProfile.objects.all()
    return render(request, 'mentor/userdetails.html', {'users': users})