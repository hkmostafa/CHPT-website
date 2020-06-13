from django.urls import path

from . import views

urlpatterns = [    
    path('contactus/', views.ContactView, name='contact'),
]