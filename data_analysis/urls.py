from django.urls import path
from . import views

urlpatterns = [
    path('', views.analysis, name='analysis'),
    path('select-data/', views.select_data, name='select_data'),
    path('create-analysis/', views.create_analysis, name='create_analysis'),
    path('visualization/<int:analysis_id>/', views.visualization, name='visualization'),
    path('decision/<int:analysis_id>/', views.decision_making, name='decision_making'),
    path('statistical-table/<int:analysis_id>/', views.statistical_table, name='statistical_table'),
    path('get_selected_data/', views.get_selected_data, name='get_selected_data'),
]