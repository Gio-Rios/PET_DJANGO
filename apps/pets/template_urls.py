"""URLs para views de template (frontend HTML) de pets."""
from django.urls import path

from apps.pets.views.template_views import (
    AboutView,
    HomeView,
    MyPetsPageView,
    PetCreateView,
    PetDetailView,
    PetListView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='page-home'),
    path('sobre/', AboutView.as_view(), name='page-about'),
    path('pets/', PetListView.as_view(), name='page-pet-list'),
    path('pets/create/', PetCreateView.as_view(), name='page-pet-create'),
    path('pets/<int:pk>/', PetDetailView.as_view(), name='page-pet-detail'),
    path('pets/mypets/', MyPetsPageView.as_view(), name='page-mypets'),
]
