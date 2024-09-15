from django.urls import path
from . import views

urlpatterns = [
    path('datasets/', views.dataset_list, name='dataset_list'),
    path('datasets/<int:pk>/', views.dataset_detail, name='dataset_detail'),
    path('datasets/<int:dataset_pk>/create_analysis/', views.create_analysis, name='create_analysis'),
    path('analysis/<int:pk>/', views.analysis_detail, name='analysis_detail'),
    path('analysis/<int:pk>/export_pdf/', views.export_pdf, name='export_pdf'),
    path('search/', views.search_datasets, name='search_datasets'),
    path('swot/create/', views.create_swot_analysis, name='create_swot_analysis'),
    path('swot/<int:pk>/', views.swot_analysis_detail, name='swot_analysis_detail'),
    path('cba/create/', views.create_cost_benefit_analysis, name='create_cost_benefit_analysis'),
    path('cba/<int:pk>/', views.cost_benefit_analysis_detail, name='cost_benefit_analysis_detail'),
    path('mcda/create/', views.create_mcda_analysis, name='create_mcda_analysis'),
    path('mcda/<int:pk>/', views.mcda_analysis_detail, name='mcda_analysis_detail'),
]