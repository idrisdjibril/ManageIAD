from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Dataset, Analysis

class DataAnalysisTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.dataset = Dataset.objects.create(
            name='Test Dataset',
            description='A test dataset',
            file='path/to/test/file.csv',
            user=self.user
        )
        self.analysis = Analysis.objects.create(
            dataset=self.dataset,
            name='Test Analysis',
            description='A test analysis',
            chart_type='bar',
            x_axis='X',
            y_axis='Y',
            user=self.user
        )

    def test_dataset_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dataset_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Dataset')

    def test_dataset_detail_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dataset_detail', args=[self.dataset.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Dataset')

    def test_create_analysis_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('create_analysis', args=[self.dataset.id]))
        self.assertEqual(response.status_code, 200)

    def test_analysis_detail_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('analysis_detail', args=[self.analysis.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Analysis')

    def test_export_pdf_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('export_pdf', args=[self.analysis.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_search_datasets_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('search_datasets'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Dataset')

    def test_unauthenticated_access(self):
        response = self.client.get(reverse('dataset_list'))
        self.assertRedirects(response, '/login/?next=' + reverse('dataset_list'))
