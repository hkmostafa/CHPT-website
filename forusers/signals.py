from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.shortcuts import render, redirect


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()

# users_without_profile = User.objects.filter(profile__isnull=True)
# for user in users_without_profile:
#     Profile.objects.create(user=user)