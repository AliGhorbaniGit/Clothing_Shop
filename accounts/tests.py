from django.test import TestCase
from django.shortcuts import reverse
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

from accounts.models import CustomUser


class AccountsTest(TestCase):
    def setUp(self):
        self.test_user = CustomUser.objects.create(username="Ali", password='1axas5xa', email='AAA@gmail.com')
        # login = self.client.get(reverse('account_login'))
        # user = get_user_model().objects.create(username="Ali")
        # user.set_password("psst")
        # user.save()
        # EmailAddress.objects.create(
        #     user=user,
        #     email="raymond.penners@example.com",
        #     primary=True,
        #     verified=True,
        # )
        self.req = self.client.post(
            reverse("account_login"),
            {"login": "ALi", "password": "psst"},
        )
        req = self.client.get(reverse('account_login'))

    def test_login_view(self):
        req = self.client.get(reverse('account_login'))
        self.assertEquals(req.status_code, 200)

        req_2 = self.client.get('/account/login/')
        self.assertEquals(req_2.status_code, 200)

        req_2 = self.req
        self.assertEquals(req_2.status_code, 200)

    def test_account_signup_view(self):
        req = self.client.get(reverse('account_signup'))
        self.assertEquals(req.status_code, 200)

        req_2 = self.client.get('/account/signup/')
        self.assertEquals(req_2.status_code, 200)

    def test_account_logout_view(self):
        req = self.client.get(reverse('account_logout'))
        self.assertEquals(req.status_code, 302)

    # allauth has his own tests so for more test, run all_auth tests
