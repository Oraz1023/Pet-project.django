import json

from django.http import request
from django.test import TestCase
from django.urls import reverse, reverse_lazy

class GetCookieTestCase(TestCase):
    def test_get_cookie_view(self):
        response=self.client.get(reverse('myauth:cookie-get'))
        print(response.content.decode('utf-8'))
        self.assertContains(response, "Cookie value" , status_code=200)



class DictionaryViewTestCase(TestCase):
    def test_dictionary_view(self):
        response=self.client.get(reverse('myauth:dictionary'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json',)
        expected_data={"dictio":"nary", "spam":"eggs"}
        # recived_data=json.loads(response.content.decode('utf-8'))
        # self.assertEqual(recived_data,expected_data)
        self.assertJSONEqual(response.content.decode('utf-8'), expected_data)




