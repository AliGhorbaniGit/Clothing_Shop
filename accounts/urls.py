from django.urls import path
from .views import Login, log_out, sign_in, pass_reset


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signin/', sign_in, name='sign_in'),
    path('passwordreset/',pass_reset, name="password_reset"),
    path('logout/', log_out, name="logout")
]



