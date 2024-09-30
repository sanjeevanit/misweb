from django.test import TestCase, Client
from django.urls import reverse
from mistech.models import Course  # Import your Course model

class PDFViewTest(TestCase):
    def setUp(self):
        # Create some sample courses for testing
        self.course1 = Course.objects.create(c_name="Course 1", c_code="C001", c_type="Type A")
        self.course2 = Course.objects.create(c_name="Course 2", c_code="C002", c_type="Type B")
        # Create a Django test client
        self.client = Client()

    def test_pdf_generation_with_search_query(self):
        # Test PDF generation with a search query
        url = reverse('c_pdf') + '?search=national'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Add assertions to check if the generated PDF content matches the expected data

    def test_pdf_generation_with_selected_ids(self):
        # Test PDF generation with selected IDs
        url = reverse('c_pdf') + '?selected_ids=1,2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Add assertions to check if the generated PDF content matches the expected data

    def test_pdf_generation_with_search_query_and_selected_ids(self):
        # Test PDF generation with both search query and selected IDs
        url = reverse('c_pdf') + '?search=national&selected_ids=1,2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Add assertions to check if the generated PDF content matches the expected data

    def test_pdf_generation_without_parameters(self):
        # Test PDF generation without any parameters
        url = reverse('c_pdf')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
