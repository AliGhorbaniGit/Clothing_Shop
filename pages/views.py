from django.views import generic
from .models import Package, Comment


class ShowPackages(generic.ListView):
    model = Package
    template_name = 'pages/home.html'
    context_object_name = 'package'
