from django.urls import path
from . import views

urlpatterns = [
    path('', views.starter, name='download'),
    path('d/<addrid>/', views.download, name='download_f'),
    path('dp/<addrid>/', views.download_preload, name='download_f_plus'),
    path('search/<addr>/', views.search, name='search'),
]
