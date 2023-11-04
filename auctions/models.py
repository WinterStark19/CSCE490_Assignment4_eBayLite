from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length = 60)

    def __str__(self):
        return f"{self.title}"
    
class Auction(models.Model):
    title = models.CharField(max_length = 60)
    description = models.TextField(max_length = 480)
    price = models.DecimalField(max_digits = 9, decimal_places = 2, default = 0.00, validators = [MinValueValidator(0)])
    imageurl = models.CharField(max_length = 1000, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_seller")
    closed = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    update_date = models.DateTimeField(auto_now=True, null=True, verbose_name="Updated At")

    def __str__(self):
        return f"Auction #{self.id} /n Title: {self.title} /n Seller: {self.seller} /n Closed: {self.closed}"
    