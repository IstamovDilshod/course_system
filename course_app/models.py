from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import FileExtensionValidator


def lesson_video_upload_path(instance, filename):
    # Fayl: media/courses/{course_id}/lessons/{lesson_id}/{filename}
    return f"courses/{instance.lesson.course.id}/lessons/{instance.lesson.id}/{filename}"


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.course.title} → {self.title}"



class LessonVideo(models.Model):
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name='video'
    )
    file = models.FileField(
        upload_to=lesson_video_upload_path,
        validators=[FileExtensionValidator(['mp4', 'mov', 'avi', 'mkv', 'webm'])]
    )
    duration = models.PositiveIntegerField(default=0, help_text="Sekundlarda")
    size = models.PositiveBigIntegerField(default=0, help_text="Baytlarda")
    is_processed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video → {self.lesson.title}"

    def get_size_mb(self):
        return round(self.size / (1024 * 1024), 2)

    def get_duration_formatted(self):
        m, s = divmod(self.duration, 60)
        return f"{m:02d}:{s:02d}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField()  # 1–5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} → {self.course.title} ({self.rating}⭐)"