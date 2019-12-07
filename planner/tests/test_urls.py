from django.test import SimpleTestCase
from django.urls import reverse, resolve
from registration.views import register

class TestUrls(SimpleTestCase):

    def test_landing_page_url(self):
        response = self.client.get(reverse('planner:landing_page'))
        self.assertEqual(response.status_code, 200)

    # A 302 indicates a (temporary) redirect.
    # "The requested resource resides temporarily under a different URI"
    # The response's status code in the following test function is 302
    # becasue the corresponding view requires the user to be logged in
    def test_projects_listed_url(self):
        response = self.client.get(reverse('planner:projects_listed'))
        self.assertEqual(response.status_code, 302)

    def test_register_url(self):
        url = reverse("register") # /register/
        func = resolve(url)[0] # func called for resolving a url 
        self.assertEquals(func, register)


