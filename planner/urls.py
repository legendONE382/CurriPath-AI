from django.urls import path

from .views import curriculum_view

urlpatterns = [
    path('', curriculum_view, name='home'),
]
