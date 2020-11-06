from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='requests_view'),
    path('delete/', views.delete, name='requests_delete')
]