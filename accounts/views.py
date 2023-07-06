from django.views import generic

from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationFrom


class Login(generic.CreateView):
    form_class = CustomUserCreationFrom
    template_name = 'accounts/login.html'
    context_object_name = 'form'





