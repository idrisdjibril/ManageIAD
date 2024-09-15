# data_import/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'dhsi2', views.DHSI2ViewSet)

urlpatterns = [
    path('', views.data_table, name='data_table'),
    path('export/', views.export_pdf, name='export_pdf'),
    path('api/', include(router.urls)),
]