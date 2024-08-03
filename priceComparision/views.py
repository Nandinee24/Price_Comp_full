# priceComparision/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to the Price Comparison App!")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('product_scraper.urls')),  # Make sure this is correct
]
