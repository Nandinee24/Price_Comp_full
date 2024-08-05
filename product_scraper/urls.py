from django.urls import path
from .views import scrape_view, search_product

urlpatterns = [
    path('', scrape_view, name='scrape'),
    path('search/', search_product, name='search_product'),
]
