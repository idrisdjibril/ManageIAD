from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from .views import dashboard_admin, dashboard_director, dashboard_agent, data_table, visualization, decision_making, user_list, compose, edit_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('', RedirectView.as_view(url='/auth/home/', permanent=True)),
    path('data_import/', include('data_import.urls')),
    path('data_analysis/', include('data_analysis.urls')),
    path('collaboration/', include('collaboration.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/admin/', dashboard_admin, name='dashboard_admin'),
    path('dashboard/director/', dashboard_director, name='dashboard_director'),
    path('dashboard/agent/', dashboard_agent, name='dashboard_agent'),
    path('data/', data_table, name='data_table'),
    path('visualization/', visualization, name='visualization'),
    path('decision/', decision_making, name='decision_making'),
    path('users/', user_list, name='user_list'),
    path('compose/', compose, name='compose'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]