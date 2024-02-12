from django.urls import path
from .views import user_to_admin_contact, all_new_contact, AdminAnswerContact

app_name = 'contactus'

urlpatterns = [
    path('usercontact/', user_to_admin_contact, name='user_to_admin_contact'),
    path('NewContact/', all_new_contact, name='all_new_contact'),
    path('AdminContact/<int:pk>', AdminAnswerContact.as_view(), name='admin_answer_contact'),
]
