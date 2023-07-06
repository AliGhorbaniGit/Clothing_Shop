from django.shortcuts import render,get_object_or_404
from django.views import generic
from .models import Package, Comment


class ShowPackages(generic.ListView):
    model = Package
    template_name = 'pages/home.html'
    context_object_name = 'package'


def package_detail_view(request,pk):
    package = get_object_or_404(Package, pk=pk)
    comment = package.package.all()

    return render(request,'pages/package_view.html', {"package":package, "comment": comment})
