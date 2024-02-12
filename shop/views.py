from copy import deepcopy
from django import http
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils.translation import gettext as _
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from accounts.forms import UserInformationChangeForm
from accounts.models import CustomUser
from .models import Product, Comment, ReplyComment, ProductColorSizeCount
from .forms import CommentForm, CommentEditForm, CommentReplyForm, SearchForm
from cart.forms import AddToCartForm
from cart.cart import Cart
from cart.favorite import Favorite
from orders.models import Order, OrderItem
from contactus.models import ContactUs
from .models import AdminAwareness


def all_product_view(request):
    """  show all products  """

    check = False
    admin_awareness = AdminAwareness.objects.all()
    products = Product.objects.all()
    if len(products) == 0:
        return render(request, 'shop/product_list.html')

    else:
        # check product availability
        for product in products:
            targets = product.size_color_count.all()
            if len(targets) == 0:
                Product.objects.filter(id=product.id).update(available=False)

                for id in admin_awareness:
                    if str(product.id) == id.access_way:
                        check = True
                        break
                    else:
                        check = False

                if check == False:
                    AdminAwareness.objects.create(sender='site support ',
                                                  subject='Product get unavailable',
                                                  access_way=product.id, )

                # if all(product.id != i.access_way for i in admin_awareness):
                # if product.id not in admin_awareness.access_way:
                #     AdminAwareness.objects.create(sender='site support ',
                #                                   subject='Product get unavailable',
                #                                   access_way=product.id,)

            else:
                for item in targets:
                    print(item.how_many_color_1)
                    if item.how_many_color_1 and item.how_many_color_2 and item.how_many_color_3 and item.how_many_color_4 == 0:
                        Product.objects.filter(pk=item.product.id).update(available=False)
                        for id in admin_awareness:
                            if str(product.id) == id.access_way:
                                check = True
                                break
                            else:
                                check = False

                        if check == False:
                            AdminAwareness.objects.create(sender='site support ',
                                                          subject='Product get unavailable',
                                                          access_way=product.id, )
                        # if product.id not in admin_awareness.access_way:
                            # if all(product.id != i.access_way for i in admin_awareness):
                            # AdminAwareness.objects.create(sender='site support ',
                            #                               subject='Product get unavailable',
                            #                               access_way=product.id, )
                        # AdminAwareness.objects.create(sender='site support ',
                        #                               subject='Product get unavailable',
                        #                               access_way=item.product.id, )


                    # if all(getattr(item, f'how_many_color_{i}') == 0 for i in range(1, 5)):
                    #     print('555555555555555555')
                    #     Product.objects.filter(pk=item.product.id).update(available=False)
                    #     AdminAwareness.objects.create(sender='site support ',
                    #                                   subject='Product get unavailable',
                    #                                   access_way=item.product.id, )
                    else:

                        # Product.objects.filter(pk=item.product.id).update(available=True)
                        # AdminAwareness.objects.create(sender='site support ',
                        #                               subject='Product get unavailable',
                        #                               access_way=item.product.id,)
                        break

        # QuerySet containing all objects to be paginated
        products = Product.objects.filter(show=True).order_by('-available')

        # Number of objects to be displayed per page
        objects_per_page = 3

        # Create a Paginator object
        paginator = Paginator(products, objects_per_page)

        # Get the current page number from the request
        page_number = request.GET.get('page')

        # Get the Page object for the current page
        page_obj = paginator.get_page(page_number)

        # Pass the Page object to the template
        return render(request, 'shop/product_list.html', {'products': page_obj})


def product_detail_view(request, pk):
    """     THIS VIEW IS TO SHOW A PRODUCT IN DETAIL, AND ALSO GET USER COMMENTS    """
    # get product
    product = get_object_or_404(Product, pk=pk)

    # get only confirmed comment
    comments = product.comments.filter(is_confirmed=True)

    comment_form = CommentForm
    cart_form = AddToCartForm

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.author = request.user
                new_form.product = product
                new_form.save()
                messages.success(request, _('YOUR COMMENT SUBMITTED SUCCESSFULLY ,'
                                            'After the admin confirmation will be displayed. '))
            else:
                messages.success(request, _('YOUR COMMENT NOT SUBMITTED , please fill comment form correctly'))
        else:
            messages.warning(request, _('FOR SUBMIT COMMENT , FIRST OF ALL YOU MUST BE SIGNED IN'))
            return redirect(request, 'account_login')

    return render(request, 'shop/product_detail.html', {"product": product,
                                                        "comments": comments,
                                                        "comment_form": comment_form,
                                                        "cart_form": cart_form,
                                                        })


# how to make this view to post required
class CommentEdit(LoginRequiredMixin, generic.UpdateView):
    """  A VIEW TO EDIT COMMENT    """
    # def post(self, request, *args, **kwargs):
    #     if request.method != 'POST':
    #        pass
    #     else:
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    model = Comment
    template_name = 'shop/product_detail.html'
    form_class = CommentForm


@require_POST
def comment_reply_view(request):
    """   THIS VIEW GET REPLY OF COMMENT     """

    if request.user.is_authenticated:
        form = CommentReplyForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, _('YOUR reply COMMENT SUBMITTED SUCCESSFULLY'))
        else:
            messages.error(request, _('PLEASE FILL THE FIELD CORRECTLY'))

    else:
        messages.warning(request, _('FOR SUBMIT COMMENT , FIRST OF ALL YOU MUST BE SIGNED IN'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # return redirect(request, reverse('shop:product_detail', args=[request.POST.get('reply_product')]))


@require_POST
def search_product_view(request):
    """    THIS VIEW GIVES A STRING AND TRYS TO FIND IT IN PRODUCTS AND send THE RESULTS TO search_result_view """

    form = SearchForm(request.POST)
    if form.is_valid():
        search_text = form.cleaned_data['text']
        results = Product.objects.filter(title__icontains=search_text)
        if results.exists():
            return render(request, 'shop/product_list.html', {'products': results})
        else:
            messages.error(request, f'No products found for "{search_text}"')
            return all_product_view(request)


@require_POST
def admin_awareness_check(request):
    """ gives a notification info and show to admin"""
    admin_awareness_id = request.POST.get('admin_awareness_id')
    product_id = request.POST.get('product_id')

    AdminAwareness.objects.filter(id=admin_awareness_id).update(is_checked=True)
    return redirect(reverse('shop:product_detail', args=[product_id]))

# def search_result_view(request, search=None):
#     """     THIS VIEW GIVES THE RESULTS FROM search_product_view AND SHOW THEME IN TEMPLATE     """
#     if search is not None:
#         products = Product.objects.filter(id__in=search, show=True)
#         return render(request, 'shop/product_list.html', {'products': products, })
#
#     else:
#         package = Product.objects.all()
#         return render(request, 'shop/product_list.html')

# @LoginRequired
# def order_products_view(request, pk):
#     order = Order.objects.get(pk=pk)
#     items = order.items.all()
#     result = []
#     for item in items:
#         result.append(item.product.id)
#
#     return search_result_view(request, search=result)
