from django.contrib import admin
from django.urls import path, include
from .views import index  # Ensure this matches the path to the `index` view

urlpatterns = [
    path('', index, name='home'),  # Root URL pattern
    path('admin/', admin.site.urls),
    path('scrape/', include('product_scraper.urls')),  # Include product_scraper URLs
]
