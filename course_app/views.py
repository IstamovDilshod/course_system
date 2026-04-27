from rest_framework import generics, viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

import course
from .filters import CourseFilter, ReviewFilter
from .pagination import StandardPagination                  # ✅ qo'shildi
from django.shortcuts import get_object_or_404

from .models import Course, Enrollment, Lesson, Review
from .serializers import (
    RegisterSerializer, CourseSerializer,
    EnrollmentSerializer, LessonSerializer, ReviewSerializer
)
from .permissions import IsInstructor, IsOwnerOrReadOnly

User = get_user_model()


# ── Register ──────────────────────────────────────────────────────────────────
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


# ── Course ────────────────────────────────────────────────────────────────────
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination                   # ✅ ulandi

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'title']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsInstructor()]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().instructor != self.request.user:
            raise PermissionDenied("Siz bu kursni tahrirlay olmaysiz!")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.instructor != self.request.user:
            raise PermissionDenied("Siz bu kursni o'chira olmaysiz!")
        instance.delete()


# ── Lesson ────────────────────────────────────────────────────────────────────
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs.get('course_pk'))

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_pk'))
        if self.request.user != course.instructor:
            raise PermissionDenied("Faqat kurs egasi dars qo'sha oladi!")
        serializer.save(course=course)

    def perform_update(self, serializer):
        if self.request.user != self.get_object().course.instructor:
            raise PermissionDenied("Faqat kurs egasi darsni tahrirlay oladi!")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.course.instructor:
            raise PermissionDenied("Faqat kurs egasi darsni o'chira oladi!")
        instance.delete()


# ── Review ────────────────────────────────────────────────────────────────────
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'delete']

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Review.objects.filter(course_id=self.kwargs.get('course_pk'))

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(),IsInstructor()]

    def perform_create(self, serializer):
        course = Course.objects.get(id=self.kwargs.get('course_pk'))
        if Review.objects.filter(user=self.request.user, course=course).exists():
            raise PermissionDenied("Siz bu kursga allaqachon baho bergansiz!")
        serializer.save(user=self.request.user, course=course)

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied("Siz faqat o'z reviewingizni o'chira olasiz!")
        instance.delete()


# ── Enrollment ────────────────────────────────────────────────────────────────
class EnrollView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class MyCourseView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)


# ── User Profile ──────────────────────────────────────────────────────────────
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "email":    request.user.email,
            "role":     request.user.role,
        })

    def patch(self, request):
        user = request.user
        if request.data.get('username'):
            user.username = request.data['username']
        if request.data.get('email'):
            user.email = request.data['email']
        if request.data.get('password'):
            user.set_password(request.data['password'])
        user.save()
        return Response({"detail": "Profil muvaffaqiyatli yangilandi!"})
    

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": f"Welcome {request.user.username}",
            "status": "active"
        })