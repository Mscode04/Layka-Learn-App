from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('register/',views.UserRegistration,name='register'),
    path('', views.LoginPage, name='login'),
    path('adminv/', views.adminView, name='admin_view'),
    path('userv/', views.userView, name='user_view'), 
    path('mentorv/', views.mentorView, name='mentor_view'), 
    path('', views.Logout, name='logout'), 
    path('users/', views.user_details, name='user_details'),
    path('users-mentor/', views.user_details_mentor, name='users-mentor'),
    path('mentors/', views.mentor_list, name='mentor_list'),
    path('mentors-std/', views.mentor_list_std, name='mentor_list_std'),
    path('add-mentor/', views.add_mentor, name='add_mentor'),
    path('add-course/', views.add_course, name='add_course'),
    path('courses/', views.course_list, name='course_list'),
    path('course_list_mentor/', views.course_list_mentor, name='course_list_mentor'),
    path('courses-std/', views.course_list_std, name='course_list_std'),
    path('course/update/<int:id>/', views.update_course, name='update_course'),
    path('course-mentor/<int:id>/', views.update_course_mentor, name='update_course_mentor'),
    path('allocate-mentor/<int:user_id>/', views.allocate_mentor, name='allocate_mentor'),
    path('checkout/<int:course_id>/', views.create_checkout_session, name='checkout'),
    path('purchase-students/', views.purchase_students, name='purchase_students'),
    path('rating-page-mentor/', views.rating_page, name='rating_page-mentor'),
    path('endrollment/', views.enrollment_page, name='endrollment'),
    path('endrollment-std/', views.select_student_course, name='endrollment-std'),
    path('course-success/', views.suc_course, name='course-success'),
    path('mycourse_list_std/', views.mycourse_list_std, name='mycourse_list_std'),
    path('progress/', views.student_progress, name='progress'),
    path('progressad/', views.student_progress_admin, name='progressad'),
    path('progressmentor/', views.student_progress_mentor, name='progressmentor'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)