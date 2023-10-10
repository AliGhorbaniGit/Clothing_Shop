from itertools import chain

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils.translation import gettext as _

from .models import Package, Comment, ReplyComment
from .forms import CommentForm, CommentUdateForm, CommentReplyForm
from cart.forms import AddToCartForm
from cart.favorite import Favorite
from orders.models import Order


class ShowPackages(generic.ListView):
    """ A VIEW TO SHOW ALL PRODUCTS """

    model = Package
    template_name = 'pages/product_list.html'
    context_object_name = 'package'
    paginate_by = 8


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
    comments = package.package.all()

    # comment_reply = {}
    # for com in comments:
    #
    #     comment_reply[com.text] += {com.commentreply.all()}
    #     print('fffffffffff')
    #     print(comment_reply[com])

    # final_list = list(chain(comments, comment_reply))

    # print('**************************')
    # for ccc in comments['reply']:
    #     print(ccc.text)

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
                                                       "comment": comments,
                                                       "comment_form": comment_form,
                                                       "cart_form": cart_form,
                                                       # 'comment_reply':comment_reply,
                                                       # "final_list": final_list,
                                                       })


class CommentUpdate(generic.UpdateView):
    model = Comment
    template_name = 'pages/package_view.html'
    form_class = CommentUdateForm
    # success_url = reverse('package_detail_view')


def comment_reply_view(request):
    comment_reply_form = CommentReplyForm

    print('77777777777777777777777comment_reply_view')
    if request.user.is_authenticated:
        form = comment_reply_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('YOUR reply COMMENT SUBMITTED SUCCESSFULLY'))
            print(comment_reply_form)
            print(request.POST.get('text'))
            print(request.POST.get('reply_author'))
            print(request.POST.get('reply_package_name'))
            print(request.POST.get('comment_name'))
        else:
            print('ddddddddddddddddddd')
            print(comment_reply_form)
            print(request.POST.get('text'))
            print(request.POST.get('reply_author'))
            print(request.POST.get('reply_package_name'))
            print(request.POST.get('comment_name'))

            messages.error(request, _('enter valid COMMENT'))
    else:
        messages.warning(request, _('FOR SUBMIT COMMENT , FIRST OF ALL YOU MUST BE SIGNED IN'))
        return redirect('ShowPackages')

    return redirect(reverse('package_detail_view', args=[request.POST.get('reply_package_name')]))


def package_search_view(request):
    search_input = request.POST.get('text')
    print(f"{search_input}*************")
    try:
        print('1111111111111111111')
        first_search = get_object_or_404(Package, title=search_input)
        # Package.objects.get(title=search_input)
        print('------------------------------')
        return redirect(reverse('package_detail_view', args=[first_search.id]))
    except:
        pass

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


    except:
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


def profile_view(request):
    """ getting user favorites information"""
    favorite = Favorite(request)
    if favorite.is_empty() or False:
        messages.success(request, _('your wish list is empty '))
        return redirect('ShowPackages')
    product_ids = favorite
    favorites = Package.objects.filter(id__in=product_ids)

    """ getting user comments """
    comment = request.user.author.all()
    reply_comment = request.user.reply_author.all()

    """ getting user order and order items information"""
    # orders = request.user.user_order.all()
    # print('pppppppppppppppppppppppppppp')
    # print(orders)
    # for item in orders:
    #     print('444444444444444444444')
    #     print(item)
    # order_items = []
    # for order in orders:
    #     order_items += order.items.all()

    orders = request.user.user_order.all()
    print('pppppppppppppppppppppppppppp')

    ordser_and_items = {}

    ordser_and_items['order'] = {}
    for order in orders:
        for ord in order.items.all():
            ordser_and_items['order'] = ord

    # for order in orders:
    #     # order['order_items']
    #     ordser_and_items['order_items'] = order.items.all()
    messages.success(request, _('click on any link to see more  detail'))
    return render(request, 'profile.html',
                  {'favorites': favorites,
                   'comment': comment,
                   'ordser_and_items': ordser_and_items,
                   'orders': orders,
                   'reply_comment': reply_comment,
                   })


def order_products_view(request, pk):
    order = Order.objects.get(pk=pk)
    items = order.items.all()
    result = []
    for item in items:
        result.append(item.product.id)
        # result.append(package.id)

    return show_all_package(request, search=result)
