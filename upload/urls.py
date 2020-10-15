from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload, name='add_addr'),
    path('search/<address>/', views.search_api, name='search'),
]
