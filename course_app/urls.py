from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import MyTokenObtainPairView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from .views import DashboardView
from django.urls import re_path
from django.views.generic import TemplateView

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


schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(r'^.*$', TemplateView.as_view(template_name='index.html')),

    # Auth
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),

    # Profile
    path('profile/', UserProfileView.as_view(), name='profile'),

    # Enrollment
    path('enroll/', EnrollView.as_view(), name='enroll'),
    path('my-courses/', MyCourseView.as_view(), name='my-courses'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Courses + nested (lessons, reviews)
    path('', include(router.urls)),
    path('', include(course_router.urls)),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),


       # boshqa API routelar
    # path('api/...')

  
]