from django.urls import path
from . import views

urlpatterns = [
    path('', views.collaboration, name='collaboration'),
    path('inbox/', views.inbox, name='inbox'),
    path('compose/', views.compose, name='compose'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('sent/', views.sent, name='sent'),
    path('search/', views.search_results, name='search_results'),
    path('folders/', views.folders, name='folders'),
    path('groups/', views.groups, name='groups'),
    path('calendar/', views.calendar, name='calendar'),
    path('get_events/', views.get_events, name='get_events'),
    path('tasks/', views.tasks, name='tasks'),
    path('update_task/', views.update_task, name='update_task'),
]