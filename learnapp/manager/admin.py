from django.contrib import admin
from .models import MentorProfile, UserProfile, LoginTable,Course,CourseFile,Payment,Rating,CourseEnrollment

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(LoginTable)
admin.site.register(MentorProfile)
admin.site.register(Course)
admin.site.register(CourseFile)
admin.site.register(Payment)
admin.site.register(Rating)
admin.site.register(CourseEnrollment)


