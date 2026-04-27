# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

@receiver(post_save, sender=LessonVideo)
def set_video_meta(sender, instance, created, **kwargs):
    if created and instance.file:
        size = instance.file.size
        LessonVideo.objects.filter(pk=instance.pk).update(size=size)