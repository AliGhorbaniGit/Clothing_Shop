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


def show_all_package(request, search=None):
    if search is not None:
        package = Package.objects.filter(id__in=search)
        return render(request, 'pages/product_list.html', {'package': package, })

    else:
        package = Package.objects.all()
        return render(request, 'pages/product_list.html', {'package': package, })


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
    search_input = request.POST.get('text')
    print(f"{search_input}*************")
    try:
        if len(search_input) > 2:

            all_package = Package.objects.all()
            print('++++++++++++++++++')

            result = []
            symbol = []
            for package in all_package:  # must be 0
                print('2222222222222222222222')
                print(package)
                # package = num
                # symbol += search_input[letter]
                counter = 0
                for item in range(0, 3):
                    print('33333333333333333333333333')
                    if package.title[item] == search_input[item]:
                        counter += 1
                        print('444444444444')
                    if counter > 2:
                        print('555555555555555')
                        result.append(package.id)
            print('////////////////////////////')
            print(result)

        # return result
        else:
            result = None


    except :
        print('uuuuuuuuuuuuuuuuuuuuuuuuuuu')
        result = None

    if result:

        print(f"*************{search_input}")
        return show_all_package(request, search=result)

    else:
        if len(search_input) < 3:
            messages.success(request, _('enter more than 2 character'))
            return redirect('ShowPackages')

        else:
            messages.success(request, _(f' no result for  {search_input} ) '))
            return redirect('ShowPackages')

    # search_input  = request.POST.get('text')
    # print(f"{search_input}*************")
    # try:
    #     search = Package.objects.get(title=search_input)
    #     print('++++++++++++++++++')
    #     print(search_input[0])
    #
    # except Package.DoesNotExist :
    #     search=None
    # if search:
    #     print('***********hi')
    #
    #     print(f"*************{search}")
    #     return redirect('package_detail_view', search.id)
    #
    # else:
    #     messages.success(request, _(f' no result for  {poll} , maybe have a syntax error :) '))
    #
    #     return redirect('ShowPackages')
