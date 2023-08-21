from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

from allauth.account.views import LoginView

from cart.cart import Cart
from cart.context_processors import cart
from accounts.models import CustomUser
from config import settings
from pages.models import Package
from .forms import OrderForm


# from cart.tests import CartTest


class OrderViewsTest(TestCase):

    def setUp(self):
        login = self.client.get(reverse('account_login'))

        user = get_user_model().objects.create(username="@raymond.penners")
        user.set_password("psst")
        user.save()
        EmailAddress.objects.create(
            user=user,
            email="raymond.penners@example.com",
            primary=True,
            verified=True,
        )
        self.resp = self.client.post(
            reverse("account_login"),
            {"login": "@raymond.penners", "password": "psst"},
        )
        # car = CartTest.test_add_to_cart_view_by_url_name
        # self.test_user = CustomUser.objects.create(password='1axas5xa', email='aghor@gmail.com')
        self.test = Package.objects.create(title='test', price=2, image='image/url', description='description', )
        self.test2 = Package.objects.create(title='testt', price=2, image='image/urll', description='ddescription', )
        add = self.client.get(reverse('add_to_cart', args=[self.test2.id]))
        add = self.client.post(reverse('add_to_cart', args=[self.test.id]))
        self.client.post(f'/cart/add/{self.test.id}/', {'quantity': 1, 'inplace': False})
        # self.assertRedirects(
        #     self.resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
        # )

        self.order_form = {'first_name': 'ali', 'last_name': 'ghorbani', 'phone_number': '09215994828',
                           'address': 'some where', 'order_notes': 'nothing', }

    def test_order_create_view_by_url_and_not_login(self):
        """  here must comment the login process in setUp   """
        res = self.client.get('/order/create/')
        self.assertEquals(res.status_code, 302)

    def test_order_create_view_by_url_name_when_len_cart_be_0(self):
        add = self.client.get(reverse('add_to_cart', args=[self.test.id]))
        # car = CartTest.test_add_to_cart_view_by_url_name

        res = self.client.get(reverse('order_create'))
        self.assertEquals(res.status_code, 302)
        # i must change phon number

    # def test_order_create_view_by_url_name_when_len_cart_is_not_0_and_request_method_is_POST(self):
    #     res = self.client.get(reverse('order_create'))
    #     self.assertRedirects(
    #         self.resp, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
    #     )
    #     add = self.client.get(reverse('add_to_cart', args=[self.test.id]))
    #     self.client.post(reverse("order_create"),{self.order_form })
    #     self.assertEquals(res.status_code, 302)
