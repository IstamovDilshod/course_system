from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import MyTokenObtainPairView
from .views import (
    CourseViewSet, RegisterView, EnrollView,
    MyCourseView, UserProfileView, LessonViewSet, ReviewViewSet
)

# ── Asosiy router ────────────────────────────────────────────────────────────
router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

# ── Nested router: /courses/{course_pk}/lessons/ ─────────────────────────────
course_router = routers.NestedDefaultRouter(router, r'courses', lookup='course')
course_router.register(r'lessons', LessonViewSet, basename='course-lessons')
course_router.register(r'reviews', ReviewViewSet, basename='course-reviews')

urlpatterns = [
    # Auth
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),

    # Profile
    path('profile/', UserProfileView.as_view(), name='profile'),

    # Enrollment
    path('enroll/', EnrollView.as_view(), name='enroll'),
    path('my-courses/', MyCourseView.as_view(), name='my-courses'),

    # Courses + nested (lessons, reviews)
    path('', include(router.urls)),
    path('', include(course_router.urls)),
]