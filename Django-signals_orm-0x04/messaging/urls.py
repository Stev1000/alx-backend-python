# messaging/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('delete_user/', views.delete_user, name='delete_user'),
    path('account_deleted/', views.account_deleted, name='account_deleted'),

]
