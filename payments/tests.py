from django.test import TestCase
from django.urls import reverse

from orders.tests import OrderTests


class PaymentsTests(TestCase):
    def setUp(self):
        order_test = OrderTests()
        order_test.test_order_create_by_as_user_logined_and_len_cart_not_equall_0_and_request_equall_post_by_valid_data

    # def test_payment_process(self):
    #     req = self.client.get('/payment/process/')
    #     req_2 = self.client.get(reverse('payments:payment_process'))
    #     self.assertEqual(req.status_code, 200)
    #     self.assertEqual(req_2.status_code, 200)
