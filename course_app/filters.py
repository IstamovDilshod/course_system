# course_app/filters.py
import django_filters
from .models import Course, Review

class CourseFilter(django_filters.FilterSet):
    # Narx oralig'i
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Sarlavha bo'yicha (qisman qidirish)
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    
    # Instructor bo'yicha
    instructor = django_filters.NumberFilter(field_name='instructor__id')

    class Meta:
        model = Course
        fields = ['title', 'min_price', 'max_price', 'instructor']


class ReviewFilter(django_filters.FilterSet):
    # Reyting bo'yicha
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')

    class Meta:
        model = Review
        fields = ['min_rating', 'max_rating']