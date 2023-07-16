from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from .models import Package, Comment
from .forms import CommentForm


class ShowPackages(generic.ListView):
    model = Package
    template_name = 'pages/home.html'
    context_object_name = 'package'


def package_detail_view(request, pk, **kwargs ):
    package = get_object_or_404(Package, pk=pk)
    comment = package.package.all()
    comment_form = CommentForm

    if request.method == 'GET':
        return render(request, 'pages/package_view.html', {"package": package,
                                                           "comment": comment,
                                                           "comment_form": comment_form})

    else:
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.author = request.user
                new_form.package_name = package
                new_form.save()
                return render(request, 'pages/package_view.html', {"package": package, "comment": comment, "comment_form": comment_form})

        else:
            return redirect('account_login')


