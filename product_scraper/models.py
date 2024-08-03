from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_flipkart = models.CharField(max_length=255, default="Not available")
    price_amazon = models.CharField(max_length=255, default="Not available")
    price_croma = models.CharField(max_length=255, default="Not available")

    def __str__(self):
        return f'{self.product.name} - {self.price_flipkart}/{self.price_amazon}/{self.price_croma}'
