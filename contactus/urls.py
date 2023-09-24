from django.urls import path
from .views import user_to_admin_contact, admin_to_user_new_contact, AdminToNewUserContact

urlpatterns = [
    path('contactAdmin/', user_to_admin_contact, name='user_to_admin_contact'),
    path('NewContact/', admin_to_user_new_contact, name='admin_to_user_new_contact'),
    path('AdminContact/<int:pk>', AdminToNewUserContact.as_view(), name='admin_to_new_user_contact')
]
