from django.contrib.messages import get_messages
from django.test import TestCase
from django.shortcuts import reverse

from shop.models import Product


class CartTest(TestCase):
    def setUp(self):
        self.test = Product.objects.create(
            title='test',
            price=2,
            image='image/products_image/t-shirt.jpg',
            show=True,
        )

    def test_add_to_cart_view_by_valid_form(self):
        """ this test post data to add_to_cart url and check this work correctly or not """
        data = {'size': 'size1', 'color': 'color1', 'quantity': 2}
        res = self.client.post(reverse('cart:add_to_cart', args=[self.test.id]), data)
        self.assertEqual(res.status_code, 302)

        messages = [m.message for m in get_messages(res.wsgi_request)]
        self.assertIn('product added to your cart successfully', messages)
        res_2 = self.client.post(f'cart/add/<{self.test.id}>/', data)
        self.assertEqual(res_2.status_code, 302)

    def test_add_to_cart_invalid_form(self):
        """ this test post invalid data to add_to_cart url and expect an error message """
        data = {
            'quantity': 1,
            # Missing color and size
        }
        response = self.client.post(reverse('cart:add_to_cart', args=[self.test.id]), data)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Oops , did you forgot to choose size and color !!', messages)

    def test_cart_detail_view(self):
        """ this test cart detail view by url and url name to get 200 response code  """
        res_1 = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(res_1.status_code, 200)
        res_2 = self.client.get('/cart/cart_detail/')
        self.assertEqual(res_2.status_code, 200)
        self.assertContains(res_1, self.test.title)

    def test_remove_from_cart__view_by_url(self):
        """ this test cart removes view by url to get 302 response code  """
        res = self.client.get(f'/cart/remove/{self.test.id}/')
        self.assertEqual(res.status_code, 302)
        req = self.client.get('/cart/cart_detail/')
        self.assertNotContains(req, self.test.title)

    def test_remove_from_cart__view_by_url_name(self):
        """ this test cart removes view by url name to get 302 response code  """
        data = {'size': 'size1', 'color': 'color1', 'quantity': 2}
        self.client.post(reverse('cart:add_to_cart', args=[self.test.id]), data)
        res = self.client.get(reverse('cart:remove_from_cart', args=[self.test.id]))
        self.assertEqual(res.status_code, 302)
        req = self.client.get(reverse('cart:cart_detail'))
        self.assertNotContains(req, self.test.title)

    def test_clear_cart_url_name(self):
        """ this test cart clear view by url to get 302 response code  """

        res = self.client.get(reverse('cart:clear_cart'))
        self.assertEqual(res.status_code, 302)
        req = self.client.get(reverse('cart:cart_detail'))
        self.assertNotContains(req, self.test.title)

    def test_clear_cart__view_by_url_name(self):
        """ this test cart removes view by url to get 302 response code  """

        res = self.client.get('/cart/clear/')
        self.assertEqual(res.status_code, 302)
        req = self.client.get(reverse('cart:cart_detail'))
        self.assertNotContains(req, self.test.title)


class FavoriteTest(TestCase):
    """ this class defines to test Favorites view functions """

    def setUp(self):
        self.test = Product.objects.create(
            title='test',
            price=2,
            image='image/products_image/t-shirt.jpg',
            show=True,
        )

    def test_add_to_favorite_view(self):
        """ this test favorite add view by url and url name to get 302 response code  """

        req = self.client.get(reverse('cart:add_to_favorites', args='1'))
        self.assertEqual(req.status_code, 302)

        req_2 = self.client.get('/cart/favoriteAdd/2')
        self.assertEqual(req_2.status_code, 302)

    def test_favorite_list_view(self):
        """ this test favorites list view by url and url name to get 302 response code  """

        req = self.client.get(reverse('cart:favorites_list'))
        self.assertEqual(req.status_code, 200)

        req_2 = self.client.get('/cart/favoritelist/')
        self.assertEqual(req_2.status_code, 200)
