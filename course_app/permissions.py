from rest_framework import permissions


class IsInstructor(permissions.BasePermission):
    """Faqat instructor roli POST/PUT/DELETE qila oladi"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user and
            request.user.is_authenticated and
            getattr(request.user, 'role', None) == 'instructor'
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user and
            request.user.is_authenticated and
            obj.instructor == request.user
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Ob'ekt egasi tahrirlash/o'chirish qila oladi.
    Qolganlar faqat o'qiy oladi.
    Review, Lesson va boshqa modellarda ishlatiladi.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Review uchun — obj.user
        if hasattr(obj, 'user'):
            return obj.user == request.user

        # Course uchun — obj.instructor
        if hasattr(obj, 'instructor'):
            return obj.instructor == request.user

        # Lesson uchun — obj.course.instructor
        if hasattr(obj, 'course'):
            return obj.course.instructor == request.user

        return False