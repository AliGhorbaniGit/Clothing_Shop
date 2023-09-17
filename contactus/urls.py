from django.urls import path
from .views import user_to_admin_contact, admin_to_user_contact, AdminToUserContact

urlpatterns = [
    path('contactAdmin/', user_to_admin_contact, name='user_to_admin_contact'),
    path('Admincontact/', admin_to_user_contact, name='admin_to_user_contact'),

]
