#
# from django.test import TestCase
#
# from django.shortcuts import reverse
#
# from cart.cart import Cart
# from pages.models import Package
#
#
# class CartTest(TestCase):
#     def setUp(self):
#         self.test = Package.objects.create(
#             title='test',
#             price=2,
#             image='dshskdciwkhc',
#             description='dadadadada',
#         )
#
#     def test_add_to_cart_view_by_url(self):
#         # cart=Cart(self.client.session)
#         res = self.client.get(f'/cart/add/{self.test.id}/')
#         self.assertEqual(res.status_code, 302)
#         req = self.client.get('/cart/')
#         self.assertNotContains(req, self.test.title)
#         # self.assertEqual(len(cart), 1)
#
#     def test_add_to_cart_view_by_url_name(self):
#         res = self.client.get(reverse('add_to_cart', args=[self.test.id]))
#         self.assertEqual(res.status_code, 302)
#         req = self.client.get('/cart/')
#         self.assertNotContains(req, self.test.title)
#
#     def test_cart_detail_view_by_url(self):
#         self.client.get(reverse('add_to_cart', args=[self.test.id]))
#         res = self.client.get('/cart/')
#         self.assertEqual(res.status_code, 200)
#         self.assertNotContains(res, self.test.title)
#
#     def test_cart_detail_view_by_url_name(self):
#         self.client.get(reverse('add_to_cart', args=[self.test.id]))
#         res = self.client.get(reverse('cart_detail'))
#         self.assertEqual(res.status_code, 200)
#         self.assertNotContains(res, self.test.title)
#
#     def test_remove_from_cart__view_by_url(self):
#         self.client.get(reverse('add_to_cart', args=[self.test.id]))
#         res = self.client.get(f'/cart/remove/{self.test.id}/')
#         self.assertEqual(res.status_code, 302)
#         req = self.client.get(reverse('cart_detail'))
#         self.assertNotContains(req, self.test.title)
#
#     def test_remove_from_cart__view_by_url_name(self):
#         self.client.get(reverse('add_to_cart', args=[self.test.id]))
#         res = self.client.get(reverse('remove_from_cart', args=[self.test.id]))
#         self.assertEqual(res.status_code, 302)
#         req = self.client.get(reverse('cart_detail'))
#         self.assertNotContains(req, self.test.title)
#
#     def test_clear_cart_url_name(self):
#         res = self.client.get('/cart/clear/')
#         self.assertEqual(res.status_code, 302)
#         req = self.client.get(reverse('cart_detail'))
#         self.assertNotContains(req, self.test.title)
#         self.assertNotContains(req, "your cart get empy")
#
#     def test_clear_cart__view_by_url_name(self):
#         res = self.client.get(reverse('clear_cart'))
#         self.assertEqual(res.status_code, 302)
#         req = self.client.get(reverse('cart_detail'))
#         self.assertNotContains(req, self.test.title)
#         self.assertNotContains(req, "your cart get empy")
