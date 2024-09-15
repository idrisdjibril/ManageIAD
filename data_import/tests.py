# data_import/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import DHSI2
from .tasks import import_csv_data

class DataImportTestCase(TestCase):
    def setUp(self):
        DHSI2.objects.create()

    def test_data_table_view(self):
        response = self.client.get(reverse('data_table'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'data_import/data_table.html')

    def test_export_pdf_view(self):
        response = self.client.get(reverse('export_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_import_csv_data_task(self):
        result = import_csv_data.delay()
        self.assertTrue(result.successful())