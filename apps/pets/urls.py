"""URLs da API REST para pets."""
from django.urls import path

from apps.pets.views.pet_views import (
    ConcludeAdoptionView,
    MyAdoptionsView,
    MyPetsView,
    PetDetailView,
    PetListCreateView,
    ScheduleVisitView,
)

urlpatterns = [
    path('', PetListCreateView.as_view(), name='pet-list-create'),
    path('mypets/', MyPetsView.as_view(), name='pet-mypets'),
    path('myadoptions/', MyAdoptionsView.as_view(), name='pet-myadoptions'),
    path('<int:pk>/', PetDetailView.as_view(), name='pet-detail'),
    path('<int:pk>/schedule/', ScheduleVisitView.as_view(), name='pet-schedule'),
    path('<int:pk>/conclude/', ConcludeAdoptionView.as_view(), name='pet-conclude'),
]
