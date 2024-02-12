from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from contactus.models import ContactUs


class ContactTest(TestCase):
    """ this class tests the contact app view() """

    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com')
        self.user.set_password('testpassword')
        self.user.save()
        self.user_text = 'test text'

    def test_user_to_admin_contact(self):
        """ this test try to test if request=POST and if request=GET ,
         to user_to_admin_contact view and check this work correctly or not """
        self.client.force_login(self.user)
        res_1 = self.client.get('/contactus/usercontact/')
        self.assertEqual(res_1.status_code, 200)
        res_2 = self.client.get(reverse('contactus:user_to_admin_contact'))
        self.assertEqual(res_2.status_code, 200)
        response = self.client.post(reverse('contactus:user_to_admin_contact'), {'user_text': self.user_text})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactUs.objects.filter(user=self.user, user_text=self.user_text).exists())

    def test_all_new_contact(self):
        """ this test try to test all_new_contact view to check this work correctly or not """
        self.client.force_login(self.user)
        res_1 = self.client.get('/contactus/NewContact/')
        self.assertEqual(res_1.status_code, 200)
        res_2 = self.client.get(reverse('contactus:all_new_contact'))
        self.assertEqual(res_2.status_code, 200)

    def test_all_new_contact_no_messages(self):
        response = self.client.get(reverse('contactus:all_new_contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'All Contact message was Answered , No more to do ')

    def test_all_new_contact_with_messages(self):
        # Create a new contact message
        contact = ContactUs.objects.create(user=self.user, user_text='Test message', is_new=True)
        response = self.client.get(reverse('contactus:all_new_contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_AdminAnswerContact_view(self):
        contact = ContactUs.objects.create(user=self.user, user_text='Test message', is_new=True)
        response = self.client.get(f'/contactus/AdminContact/{contact.id}')
        self.assertEqual(response.status_code, 200)

        response_2 = self.client.get(reverse('contactus:admin_answer_contact', args=[contact.id]))
        self.assertEqual(response_2.status_code, 200)
