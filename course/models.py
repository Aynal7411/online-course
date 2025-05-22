from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = CKEditor5Field('Text', config_name='default')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video_url = models.URLField(help_text="YouTube বা অন্য ভিডিও লিঙ্ক দিন")
    content = CKEditor5Field('Your Label')

    def __str__(self):
        return f"{self.course.title} - {self.title}"
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # একজন ইউজার একই কোর্সে একবারই এনরোল করতে পারবে

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
    
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {'Completed' if self.completed else 'Incomplete'}"
 