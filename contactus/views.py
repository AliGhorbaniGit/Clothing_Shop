from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required

from .forms import UserContactForm, AdminContactForm
from .models import ContactUs
from accounts.models import CustomUser


@login_required
def user_to_admin_contact(request):
    """ this view gets a message from a user """

    user = get_object_or_404(CustomUser, pk=request.user.id)

    contact = user.contactus.all()
    if request.method == 'POST':
        form = UserContactForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            cleaned_data = form.cleaned_data
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, 'Your Message Was Successfully Send ,please wait ,'
                                      'Our admins will answer you as soon as possible')
        else:
            messages.error(request, 'Your Message Was not Sent ,'
                                    ' Make sure You send message correctly')

    return render(request, 'contactus/contact_us.html', {"contact": contact})


def all_new_contact(request):
    """ this view shows all new messages from users to admin """
    new_contacts = ContactUs.objects.filter(is_new=True)
    if not new_contacts:
        messages.success(request, 'All Contact message was Answered , No more to do ')

    return render(request, 'contactus/user_new_contact.html', {"new_contacts": new_contacts})


class AdminAnswerContact(generic.UpdateView):
    """ this view gets answer from admin for user contact   """
    template_name = 'contactus/admin_contact.html'
    model = ContactUs
    form_class = AdminContactForm
    context_object_name = 'contact'
