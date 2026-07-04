"""Views que renderizam templates HTML para o frontend de pets."""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class PetListView(TemplateView):
    template_name = 'pets/list.html'


class PetCreateView(TemplateView):
    template_name = 'pets/create.html'


class PetDetailView(TemplateView):
    template_name = 'pets/detail.html'


class MyPetsPageView(TemplateView):
    template_name = 'pets/my_pets.html'
