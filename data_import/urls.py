from django.urls import path
from . import views
from .views import dashboard_admin, dashboard_director, dashboard_agent, data_table, analysis, decision_making, user_list, compose, edit_profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.data_table, name='data_table'),
    path('api/dhis2-data/', views.dhis2_data_api, name='dhis2_data_api'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/admin/', dashboard_admin, name='dashboard_admin'),
    path('dashboard/director/', dashboard_director, name='dashboard_director'),
    path('dashboard/agent/', dashboard_agent, name='dashboard_agent'),
    #path('search_data/', views.search_data, name='search_data'),
    path('advanced-search/', views.advanced_search, name='advanced_search'),
    path('api/get-columns/', views.get_columns, name='get_columns'),
    path('api/advanced-search/', views.advanced_search_api, name='advanced_search_api'),
    path('data/', data_table, name='data_table'),
    path('analysis/', analysis, name='analysis'),
    path('decision/', decision_making, name='decision_making'),
    path('users/', user_list, name='user_list'),
    path('collaboration/', compose, name='compose'),
    path('management/', edit_profile, name='edit_profile'),
]