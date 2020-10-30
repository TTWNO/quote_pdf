from django.urls import path
from . import views

urlpatterns = [
    path('', views.starter, name='download'),
    path('d/<pdfid>/', views.download, name='download_f'),
    path('search/<addr>/', views.search, name='search'),
]
