
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic

from accounts.forms import UserInformationChangeForm
from accounts.models import CustomUser
from cart.favorite import Favorite
from shop.models import Product


@login_required
def profile_view(request):
    """ THIS VIEW SHOW THE USER PROFILE   """

    """ getting user favorites information"""
    product_ids = Favorite(request)
    favorites = Product.objects.filter(id__in=product_ids)

    """ getting user'S comments """
    comments = request.user.comments.all()
    reply_comments = request.user.reply.all()

    """ getting user order and order items information"""
    orders = request.user.orders.all()

    return render(request, 'accounts/profile.html',
                  {'favorites': favorites,
                   'comment': comments,
                   'orders': orders,
                   'reply_comments': reply_comments,
                   })


class EditUserInformation(generic.UpdateView):
    model = CustomUser
    form_class = UserInformationChangeForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('accounts:profile')


def redirect_user(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
