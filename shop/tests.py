from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage

from orders.models import Order
from shop.views import comment_reply_view
from shop.forms import CommentReplyForm
from accounts.models import CustomUser

from .models import Product, Comment


class PagesViewsTest(TestCase):

    # @classmethod
    # def setUpTestData(cls):
    #     # Create a user
    #     test_user = CustomUser.objects.create_user(username='testuser1', password='12345')
    #     test_user.save()
    #
    #     # Create a product
    #     test_product = Product.objects.create(  title='test',
    #         price=2,
    #         image='image/products_image/t-shirt.jpg',
    #         show=True,)
    #     test_product.save()
    #
    #     # Create a comment
    #     test_comment = Comment.objects.create(author=test_user.id, product=test_product.id, text='Test comment',
    #                                           is_confirmed=True)
    #     test_comment.save()

    def setUp(self):
        self.product_test = Product.objects.create(
            title='test',
            price=2,
            image='image/products_image/t-shirt.jpg',
            show=True,
        )

        self.user = CustomUser.objects.create(username='testuser', email='test@example.com')
        self.user.set_password('testpassword')
        self.user.save()

    def test_all_product_view_url(self):
        res = self.client.get('')
        self.assertEquals(res.status_code, 200)
        res_2 = self.client.get(reverse('shop:product_list'))
        self.assertEquals(res_2.status_code, 200)

    def test_is_there_my_object_in_all_product_view(self):
        res = self.client.get(reverse('shop:product_list'))
        self.assertContains(res, self.product_test.title)

    def test_product_detail_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/{self.product_test.id}/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_url_accessible_by_name(self):
        req = self.client.get(reverse('shop:product_detail', kwargs={'pk': 1}))
        re_2 = self.client.get(reverse('shop:product_detail', args=[self.product_test.id]))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(re_2.status_code, 200)

    def test_view_uses_correct_template(self):
        re_2 = self.client.get(reverse('shop:product_detail', args=[self.product_test.id]))
        self.assertTemplateUsed(re_2, 'shop/product_detail.html')

    def test_is_there_test_object_in_detail_view(self):
        req_2 = self.client.get(reverse('shop:product_detail', args=[self.product_test.id]))
        self.assertContains(req_2, self.product_test.title)

    def test_post_comment_when_user_authenticated_and_comment_form_is_valid(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('shop:product_detail', args=[self.product_test.id]),
                                    {'text': 'Test comment'})
        self.assertContains(response, 'YOUR COMMENT SUBMITTED SUCCESSFULLY ,'
                                      'After the admin confirmation will be displayed. ')
        self.assertEqual(response.status_code, 200)

    def test_post_comment_when_user_authenticated_and_comment_form_is_not_valid(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('shop:product_detail', args=[self.product_test.id]),
                                    {'wrong form field name': 'Test comment'})
        self.assertContains(response, 'YOUR COMMENT NOT SUBMITTED , please fill comment form correctly')
        self.assertEqual(response.status_code, 200)

    def test_CommentEdit_view(self):
        comment_test = Comment.objects.create(
            author=self.user,
            product=self.product_test,
            text='test text',
            is_confirmed=True,
        )

        self.client.force_login(self.user)
        self.client.post(reverse('shop:product_detail', args=[self.product_test.id]),
                         {'text': 'Test comment'})
        res = self.client.post(reverse('shop:edit_comment', args=[comment_test.id]), {'text': 'edit test text'})
        self.assertEqual(res.status_code, 302)

    def test_comment_reply_view_when_user_is_not_authenticated(self):
        comment_test = Comment.objects.create(
            author=self.user,
            product=self.product_test,
            text='test text',
            is_confirmed=True,
        )

        res = self.client.post(reverse('shop:comment_reply'), {'text': 'test text',
                                                               'reply_author': self.user.id,
                                                               'reply_product': self.product_test.id,
                                                               'reply_comment': comment_test.id})

        self.assertEqual(res.status_code, 302)
        # self.assertContains(res,'FOR SUBMIT COMMENT , FIRST OF ALL YOU MUST BE SIGNED IN')
        self.assertRedirects(res, expected_url='/', )

    def test_comment_reply_view_when_user_is_authenticated_and_form_is_valid(self):
        comment_test = Comment.objects.create(
            author=self.user,
            product=self.product_test,
            text='test text',
            is_confirmed=True,
        )

        self.client.force_login(self.user)
        url = reverse('shop:comment_reply')
        res = self.client.post(url, {'text': 'test text',
                                     'reply_author': self.user.id,
                                     'reply_product': self.product_test.id,
                                     'reply_comment': comment_test.id})

        request = RequestFactory().post('/comment/reply/', {'comment_text': 'Test reply'})
        request.user = CustomUser()
        request.session = {}
        messages = FallbackStorage(request)
        request._messages = messages

        response = comment_reply_view(request)

        self.assertRedirects(res, expected_url='/', )
        self.assertEqual(response.status_code, 302)  # Assuming successful redirect
        self.assertTrue(messages.added_new)
        self.assertEqual(len(messages), 1)

    def test_comment_reply_view_when_user_is_authenticated_and_from_is_not_valid(self):
        comment_test = Comment.objects.create(
            author=self.user,
            product=self.product_test,
            text='test text',
            is_confirmed=True,
        )

        res = self.client.post(reverse('shop:comment_reply'), {'text': 'test text',

                                                               'reply_product': self.product_test.id,
                                                               'reply_comment': comment_test.id})

        self.assertEqual(res.status_code, 302)
        # self.assertContains(res,'PLEASE FILL THE FIELDS CORRECTLY')
        self.assertRedirects(res, expected_url='/', )

    def test_search_product_view_and_search_result_view_by_result(self):
        """ in this test we send a text as search text; that know that exist"""
        req = self.client.post(reverse('shop:search_product_view'), {'text': self.product_test.title})
        self.assertEqual(req.status_code, 200)

    def test_search_product_view__and_search_result_view_without_result(self):
        """ in this test we send a text as search text; that know that not exist """
        req = self.client.post(reverse('shop:search_product_view'), {'text': 'not exist'})
        self.assertEqual(req.status_code, 200)

    # def test_order_products_view_url_exists_at_desired_location(self):
    #     order = Order.objects.create(
    #         user=self.user,
    #         first_name='test user',
    #         last_name='test user',
    #         phone_number=12346789,
    #         address='test address')
    #
    #     req = self.client.post(f'/order products/{order.id}')
    #     self.assertEqual(req.status_code, 200)

    # def test_order_products_view_by_url_name(self):
    #     order = Order.objects.create(
    #         user=self.user,
    #         first_name='test user',
    #         last_name='test user',
    #         phone_number=12346789,
    #         address='test address')
    #
    #     req = self.client.post(reverse('shop:order_products', args=[order.id]))
    #     self.assertEqual(req.status_code, 200)

