from django.shortcuts import render, get_object_or_404,redirect
from .models import Course, Enrollment, Lesson, Progress
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone
from django.http import HttpResponse
from .forms import CourseForm, LessonForm
from .forms import CustomUserCreationForm


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome, {}.'.format(user.username))
            return redirect('course_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('next') or 'course_list'

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def course_list(request):
    courses = Course.objects.all()
    if request.user.is_authenticated:
       enrolled_courses = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    else:
        enrolled_courses = [] 
    return render(request, 'course_list.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses
    })

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return HttpResponseRedirect(reverse('course_list'))
@login_required
def profile_view(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    return render(request, 'profile.html', {'enrollments': enrollments})
@login_required
def mark_completed(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    progress, created = Progress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.completed = True
    progress.save()
    return JsonResponse({'status': 'success'})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    completed_lessons = Progress.objects.filter(user=request.user, lesson__in=lessons, completed=True).values_list('lesson_id', flat=True)

    return render(request, 'course_detail.html', {
        'course': course,
        'completed_lessons': completed_lessons,
    })

@login_required
def generate_certificate(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = course.lessons.all()
    completed = Progress.objects.filter(user=request.user, lesson__in=lessons, completed=True).count()
    total = lessons.count()

    if completed != total:
        return HttpResponse("Course not fully completed yet.", status=403)

    template = get_template('certificate_template.html')
    context = {
        'user': request.user,
        'course': course,
        'instructor_name': "Instructor Name",  # Replace with dynamic if you have instructor model
        'date': timezone.now().strftime('%d %B %Y')
    }

    html = template.render(context)
    response = BytesIO()
    pdf_status = pisa.CreatePDF(html, dest=response)

    if not pdf_status.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    return HttpResponse("PDF Generation Error", status=500)

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})

@login_required
def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = LessonForm()
    return render(request, 'add_course.html', {'form': form})