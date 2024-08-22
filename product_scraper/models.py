from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class PriceHistoryNew(models.Model):
    SITE_CHOICES = [
        ('flipkart', 'Flipkart'),
        ('amazon', 'Amazon'),
        ('croma', 'Croma'),
        # ('jiomart', 'JioMart'),
        # ('reliancedigital', 'Reliance Digital'),
        # ('tatacliq', 'TataCliq'),
        # ('poorvika', 'Poorvika'),
        # ('shopclues', 'ShopClues'),
        # ('paytmmall', 'Paytm Mall'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=255, choices=SITE_CHOICES , default='amazon')
    price = models.CharField(max_length=255, default="Not available")
    offers = models.TextField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    total_purchases = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.product.name} - {self.site_name} - Price: {self.price} - Rating: {self.rating}'
