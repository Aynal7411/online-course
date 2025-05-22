from django.contrib import admin
from .models import Course, Lesson, Enrollment, Progress

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    show_change_link = True

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_at')
    list_filter = ('created_at', 'instructor')
    search_fields = ('title', 'description', 'instructor__username')
    inlines = [LessonInline]
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'video_url')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    autocomplete_fields = ['course']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    list_filter = ('enrolled_at', 'course')
    search_fields = ('user__username', 'course__title')
    autocomplete_fields = ['user', 'course']
    date_hierarchy = 'enrolled_at'
    ordering = ('-enrolled_at',)

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'completed_at')
    search_fields = ('user__username', 'lesson__title', 'lesson__course__title')
    autocomplete_fields = ['user', 'lesson']
    date_hierarchy = 'completed_at'
    ordering = ('-completed_at',)

# Optional: Customize admin site branding
admin.site.site_header = "Online Course Admin"
admin.site.site_title = "Course Dashboard"
admin.site.index_title = "Welcome to the Online Course Admin Panel"
