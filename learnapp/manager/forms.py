from django import forms
from .models import CourseEnrollment, MentorProfile,Course
class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        fields = ['mentor', 'phone', 'email', 'profile_pic'] 
        
        



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'course_name', 'about', 'description', 'duration', 'price', 
            'mentor', 'part1', 'part2', 'part3', 'additional_parts', 'thumbnail'
        ]
        widgets = {
            'about': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'mentor': forms.Select(attrs={'class': 'form-control'}),
            'part1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'part2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'part3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'additional_parts': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        
        
        
class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    
    
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'student_name']  # Include the 'student_name' field
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
        
        
class SelectStudentCourseForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment  # Use the new CourseEnrollment model
        fields = ['student', 'course'] 
        
        
        
  