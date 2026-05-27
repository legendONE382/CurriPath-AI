from django.urls import path

from .views import home, generate_curriculum

urlpatterns = [
    path('', home, name='home'),
    path('generate/', generate_curriculum, name='generate_curriculum'),
]
