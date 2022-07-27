from django.urls import path
from .views import add_or_delete_follow_view

urlpatterns = [
    path('add_or_delete_follow_view',add_or_delete_follow_view,name = 'add_or_delete_follow_view'),
]
