from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='requests_view'),
    path('csv/', views.csv, name='view_downloads_csv'),
    path('all/csv/', views.csv_all, name='view_all_downloads_csv'),
]