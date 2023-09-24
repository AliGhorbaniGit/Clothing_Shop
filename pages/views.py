from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils.translation import gettext as _

from .models import Package
from .forms import CommentForm
from cart.forms import AddToCartForm


class ShowPackages(generic.ListView):
    """ A VIEW TO SHOW ALL PRODUCTS """

    model = Package
    template_name = 'pages/product_list.html'
    context_object_name = 'package'
    paginate_by = 8
    # popup_search = Package.objects.get(popup_search.value)


def package_detail_view(request, pk):
    """ THIS VIEW IS TO SHOW A PRODUCT AND ITS DETAIL"""

    package = get_object_or_404(Package, pk=pk)
    comment = package.package.all()
    comment_form = CommentForm
    cart_form = AddToCartForm
    print('4444444444444444444444444')
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


def package_search_view(request):
    poll = request.POST.get('text')
    print(f"{poll}*************")
    try:
        search = Package.objects.get(title=poll)
    except :
        search=None
    if search:
        print('***********hi')

        print(f"*************{search}")
        return redirect('package_detail_view', search.id)

    else:
        messages.success(request, _(f' no result for  {poll} , maybe have a syntax error :) '))

        return redirect('ShowPackages')
