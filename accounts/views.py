from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationFrom


class Login(generic.CreateView):
    form_class = CustomUserCreationFrom
    template_name = 'accounts/login.html'
    context_object_name = 'form'


def sign_in(request):

    if request.user.is_authenticated:
        return redirect(reverse('ShowPackages'))

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect(reverse('ShowPackages'))
        else:
            return redirect(reverse('sign_in'))
    else:
        return render(request, 'accounts/sign_in.html')


@login_required
def pass_reset(request):
    form = CustomUserChangeForm()['username'] = request.user
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CustomUserChangeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'pass chaneged')
            else:
                messages.error(request, 'u are not log in')
                return reverse('password_reset')
        else:
            messages.error(request, 'u are not log in')
            return reverse('login')

    else:
        return render(request, 'accounts/password_reset.html', {'form': form})

# its need to rewrite : i must use django_all_auth app


def log_out(request):
    logout(request)
    return redirect(reverse('ShowPackages'))
