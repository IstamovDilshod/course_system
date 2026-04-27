from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from course_app.models import Course

# Xavfsiz usul: unregister qilishdan oldin tekshiramiz
# Endi bemalol ro'yxatdan o'tkazamiz
admin.site.register(User, UserAdmin)
admin.site.register(Course)
