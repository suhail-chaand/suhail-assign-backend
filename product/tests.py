from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class ProductTests(APITestCase):
    def add_product(self):
        test_data = {
            'model': 't_model',
            'brand': 't_brand',
            'name': 't_name',
            'tagline': 't_tagline',
            'description': 't_description',
            'price': 0,
            'images': [
                {'image_url': 'https://picsum.photos/200'},
            ]
        }
        response = self.client.post('/product/addProduct', test_data, format='json')
        return response

    def test_add_product(self):
        ap_response = self.add_product()
        self.assertEqual(ap_response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_product(self):
        ap_response = self.add_product()
        response = self.client.get(reverse('get-product', kwargs={'pk': ap_response.data['data']['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
