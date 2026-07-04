"""URLs da API REST para pets."""
from django.urls import path

from apps.pets.views.pet_views import (
    AdoptedPetsView,
    CancelVisitView,
    ConcludeAdoptionView,
    DenyAdoptionView,
    GivenAwayPetsView,
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
    path('adopted/', AdoptedPetsView.as_view(), name='pet-adopted'),
    path('given-away/', GivenAwayPetsView.as_view(), name='pet-given-away'),
    path('<int:pk>/', PetDetailView.as_view(), name='pet-detail'),
    path('<int:pk>/schedule/', ScheduleVisitView.as_view(), name='pet-schedule'),
    path('<int:pk>/conclude/', ConcludeAdoptionView.as_view(), name='pet-conclude'),
    path('<int:pk>/deny/', DenyAdoptionView.as_view(), name='pet-deny'),
    path('<int:pk>/cancel-visit/', CancelVisitView.as_view(), name='pet-cancel-visit'),
]
