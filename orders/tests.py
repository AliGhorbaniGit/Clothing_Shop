from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from cart.cart import Cart
from shop.models import Product


class OrderTests(TestCase):

    def setUp(self):
        """ create a user """
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com')
        self.user.set_password('testpassword')
        self.user.save()

        """ create a product  """
        self.test = Product.objects.create(
            title='test',
            price=2,
            image='image/products_image/t-shirt.jpg',
            show=True,
        )

        """ add product to cart """
        add_to_cart_form_data = {'size': 'size1', 'color': 'color1', 'quantity': 2}
        self.client.post(reverse('cart:add_to_cart', args=[self.test.id]), add_to_cart_form_data)

        """ create data for order form  """
        self.order_form_data = {
            'first_name': 'test', 'last_name': 'test',
            'phone_number': 111111, 'address': 'test',
            'order_notes': 'test', }

    def test_order_create_view_url(self):
        req = self.client.get('/order/create/')
        self.assertEqual(req.status_code, 302)

        req_2 = self.client.get(reverse('orders:order_create'))
        self.assertEqual(req_2.status_code, 302)

    def test_order_create_by_as_user_logined_and_len_cart_not_equall_0(self):
        self.client.force_login(self.user)

        req_2 = self.client.get(reverse('orders:order_create'))
        self.assertEqual(req_2.status_code, 200)

    def test_order_create_by_as_user_logined_and_len_cart_not_equall_0_and_request_equall_post(self):
        """ here don't send data to form be invalid, and test gets status code = 200 """
        self.client.force_login(self.user)

        req_2 = self.client.post(reverse('orders:order_create'), )
        self.assertEqual(req_2.status_code, 200)

    def test_order_create_by_as_user_logined_and_len_cart_not_equall_0_and_request_equall_post_by_valid_data(self):
        """ here send data to form be valid, and the request gets redirect and gets status code = 302 """
        self.client.force_login(self.user)

        req_2 = self.client.post(reverse('orders:order_create'), self.order_form_data)
        self.assertEqual(req_2.status_code, 302)
