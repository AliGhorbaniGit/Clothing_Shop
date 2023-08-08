from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils.translation import gettext as _

from .models import Package
from .forms import CommentForm
from cart.forms import AddToCartForm


class ShowPackages(generic.ListView):
    """ A VIEW TO SHOW ALL PRODUCTS """

    model = Package
    template_name = 'pages/home.html'
    context_object_name = 'package'


def package_detail_view(request, pk):
    """ THIS VIEW IS TO SHOW A PRODUCT AND ITS DETAIL"""

    package = get_object_or_404(Package, pk=pk)
    comment = package.package.all()
    comment_form = CommentForm
    cart_form = AddToCartForm

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.author = request.user
                new_form.package_name = package
                new_form.save()
                messages.success(request, _('YOUR COMMENT SUBMITTED SUCCESSFULLY'))
        else:
            messages.warning(request, _('FOR SUBMIT COMMENT , FIRST OF ALL YOU MUST BE SIGNED IN'))
            return redirect('account_login')

    return render(request, 'pages/package_view.html', {"package": package,
                                                       "comment": comment,
                                                       "comment_form": comment_form, "cart_form": cart_form})
