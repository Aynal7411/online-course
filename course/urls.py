from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.course_list, name='course_list'),
     path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('profile/', views.profile_view, name='profile'),
    path('mark-completed/<int:lesson_id>/', views.mark_completed, name='mark_completed'),
    path('certificate/<int:course_id>/', views.generate_certificate, name='generate_certificate'),
    path('add-course/', views.add_course, name='add_course'),
    path('add-lesson/', views.add_lesson, name='add_lesson'),
]
