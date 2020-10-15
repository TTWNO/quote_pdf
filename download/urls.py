from django.urls import path
from . import views

urlpatterns = [
    path('', views.starter, name='lookup'),
    path('d/<pdfid>/', views.download, name='download'),
]
