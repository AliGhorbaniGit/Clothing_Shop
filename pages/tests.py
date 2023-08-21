# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
#
# from accounts.models import CustomUser
#
# from .models import Package, Comment
#
#
# class PagesViewsTest(TestCase):
#     def setUp(self):
#         self.test_user = CustomUser.objects.create(password='1axas5xa', email='aghor@gmail.com')
#         self.for_test = Package.objects.create(title='test', price=2, image='gsdbjhsbd')
#         self.comment_test = Comment.objects.create(author=self.test_user,
#                                                    package_name=self.for_test, text='test_text')
#
#     def test_show_package_view_by_url(self):
#         res = self.client.get('')
#         self.assertEquals(res.status_code, 200)
#
#     def test_show_package_view_by_url_name(self):
#         res = self.client.get(reverse('ShowPackages'))
#         self.assertEquals(res.status_code, 200)
#
#     def test_is_there_my_object_in_show_package_view(self):
#         res = self.client.get(reverse('ShowPackages'))
#         self.assertContains(res, self.for_test)
#
#     def test_package_detail_view_by_url(self):
#         res = self.client.get(f'/{self.for_test.id}')
#         self.assertEqual(res.status_code, 200)
#         self.assertContains(res, self.for_test.title)
#         self.assertContains(res, 'test')
#
#     def test_package_detail_view_comment_by_url_name(self):
#         res = self.client.get(reverse('package_detail_view', args=[self.for_test.id]))
#         self.assertEqual(res.status_code, 200)
#         self.assertContains(res, self.comment_test.text)
#         self.assertContains(res, 'test_text')
#


