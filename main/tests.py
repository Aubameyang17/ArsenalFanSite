from django.test import TestCase
from django.urls import reverse
from .models import SiteUsers

class UserModelTest(TestCase):

    def setUp(self):
        self.user = SiteUsers.objects.create(login="TestLogin", pasword="TestPassword", email="testemail@testemail", role="User")
        self.user.save()

    def testUserCreation(self):
        user = SiteUsers.objects.get(login="TestLogin")
        self.assertEqual(user.email, "testemail@testemail")
    #
    # def testLoginmaxlength(self):
    #     user = SiteUsers.objects.get(login="TestLogin")
    #     max_length = user._meta.get_field('login').max_length
    #     self.assertEquals(max_length, 100)


# class ProductModelTest(TestCase):
#
#     def setUp(self):
#         self.user = Product.objects.create(cost_on_sell=2000, cost_on_buy=1000, name="TestProduct", quantity_on_stock=30, picture="test/test")
#         self.user.save()
#
#     def testProductCreation(self):
#         product = Product.objects.get(name="TestProduct")
#         self.assertEqual(product.quantity_on_stock, 30)
#
#     def testNamemaxlength(self):
#         product = Product.objects.get(name="TestProduct")
#         max_length = product._meta.get_field('name').max_length
#         self.assertEquals(max_length, 100)
#
#
# class ViewTest(TestCase):
#
#     def test_view_status_code(self):
#         url = reverse('home')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_template_used(self):
#         url = reverse('history')
#         response = self.client.get(url)
#         self.assertTemplateUsed(response, 'main/History.html')


