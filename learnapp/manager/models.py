

from django.db import models
from django.db import models

class LoginTable (models.Model):
    username= models. CharField(max_length=200)
    password=models.CharField(max_length=200)
    password1=models.CharField(max_length=200)
    type=models.CharField(max_length=200)
    def __str__(self):
        return self.username

class MentorProfile(models.Model):
    mentor = models.OneToOneField(LoginTable, on_delete=models.CASCADE)  
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='mentor_profiles/', blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.mentor.username}"    

class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=5)
    std_class = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=255)
    password1 = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username





class Course(models.Model):
    course_name = models.CharField(max_length=100)
    about = models.TextField()
    description = models.TextField()
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mentor = models.ForeignKey('MentorProfile', on_delete=models.CASCADE)  # Link to MentorProfile
    part1 = models.FileField(upload_to='courses/')
    part2 = models.FileField(upload_to='courses/')
    part3 = models.FileField(upload_to='courses/')
    additional_parts = models.ManyToManyField('CourseFile', blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)  # Add thumbnail field

    def __str__(self):
        return self.course_name



class CourseFile(models.Model):
    file = models.FileField(upload_to='courses/additional_parts/')
    
    





class Payment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('failed', 'Failed')], default='failed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.full_name} for {self.course.course_name}"
    
    

class Rating(models.Model):
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=255)  # Store student name as a string
    rating = models.PositiveIntegerField() # Optional course name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating for {self.mentor} by {self.student_name}"





class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Link to the Course model
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Link to the Student (UserProfile) model
    enrollment_date = models.DateTimeField(auto_now_add=True)  # When the student enrolled in the course
    course_name = models.CharField(max_length=255, blank=True)  # Save the course name if you want to store it separately
    student_name = models.CharField(max_length=255, blank=True)  # Save the student name if needed
    
    # You can add additional fields related to the course or the enrollment, like status or progress
    status = models.CharField(max_length=50, choices=[('enrolled', 'Enrolled'), ('completed', 'Completed')], default='enrolled')

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.course_name}"







    
    
