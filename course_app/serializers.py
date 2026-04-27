from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course, Enrollment, Lesson, Review
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


# ── JWT Token (role + username qo'shilgan) ──────────────────────────────────
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['username'] = user.username  # ✅ Frontend uchun
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ── Register ─────────────────────────────────────────────────────────────────
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


# ── Lesson ───────────────────────────────────────────────────────────────────
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'order', 'created_at']
        read_only_fields = ['created_at']


# ── Review ───────────────────────────────────────────────────────────────────
class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'username', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating 1 dan 5 gacha bo'lishi kerak!")
        return value


# ── Course ───────────────────────────────────────────────────────────────────
class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'price',
            'instructor', 'instructor_name', 'created_at',
            'lessons', 'lessons_count', 'avg_rating'
        ]
        read_only_fields = ['instructor', 'created_at']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_avg_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)


# ── Enrollment ───────────────────────────────────────────────────────────────
class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'course_title', 'enrolled_at']
        read_only_fields = ['enrolled_at']