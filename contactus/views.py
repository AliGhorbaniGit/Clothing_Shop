from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.middleware.csrf import CsrfViewMiddleware
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import get_user_model
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ContactForm
from .contact import ContactUs
from .models import ContactUs
from accounts.models import CustomUser


# def user_to_admin_contact_by_session(request):
#     pass
#     user_req = request
#     contact = ContactUs(request)
#     if request.method == 'POST':
#         contact_from = ContactForm(request.POST)
#         if contact_from.is_valid():
#             # contact.add(request.POST.get('text'))
#             user_txt = contact_from.cleaned_data.get('user_txt')
#             # if request.user.is_staff:
#             #     admin_txt = contact_from.cleaned_data.get('admin_txt')
#             #     contact.add(admin_txt)
#             user_txt = contact_from.cleaned_data.get('user_txt')
#             admin_to_user_contact_by_session(user_req)
#
#             # contact.save().commit(False)
#
#     return render(request, 'contactus/contact_us.html', {"contact": contact})



# def admin_to_user_contact_by_session(request):
#     pass
    # def find_user_session(user_request):
    #     contact = ContactUs(user_request)
    #     get_user_model.user.objects.get.all()
    #
    # if 'POST':
    #     contact_from = ContactForm(request.POST)
    #     if contact_from.is_valid():
    #         # if request.user.is_staff:
    #         admin_txt = contact_from.cleaned_data.get('admin_txt')
    #         user_txt = contact_from.cleaned_data.get('user_txt')
    #
    #         contact.add(user_txt, admin_txt)
    #         contact.save()
    #         # return render(request, 'contactus/admin_contact.html', {"contact": contact})
    # # contact.add(user_txt)
    # return render(user_req, 'contactus/admin_contact.html', {"contact": contact})


@login_required
def user_to_admin_contact(request, user_id=None):
    if user_id is not None:
        user = get_object_or_404(CustomUser, pk=user_id)
    else:
        user = get_object_or_404(CustomUser, pk=request.user.id)
    print(f'**************{user.id}')
    # contact = user.objects.get(user=request.user)
    contact = user.contact_us.all()
    # contact = ContactUs.objects.all()
    if request.method == 'POST':
        print('**************im .method == ')
        form = ContactForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            print('************im in last')
            messages.success(request, 'Your Message Was Successfully Send ,'
                                      ' please wait , Our admins will answer as soon as possible')
        else:
            messages.error(request, 'Make sure You send message correctly')

    return render(request, 'contactus/contact_us.html', {"contact": contact})


def admin_to_user_contact(request):
    # contact = Contact.objects.get(user_name=request.user.id)
    users = CustomUser.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user_id')

        user_to_admin_contact(request,user_id.id)
        breakpoint()
    else:
        return render(request, 'contactus/admin_contact.html', {"users": users})


class AdminToUserContact(generic.UpdateView):
    template_name = 'contactus/admin_contact.html'
    model = ContactUs
    fields = ('admin_text',)
