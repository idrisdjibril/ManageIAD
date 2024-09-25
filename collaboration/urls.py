from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<str:recipient_username>/', views.inbox, name='inbox'),
    path('compose/', views.compose, name='compose'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('mark_as_read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('get_users/', views.get_users, name='get_users'),
]