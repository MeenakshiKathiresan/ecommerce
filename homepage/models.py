from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    trending = models.BooleanField(default=True)
    image = models.ImageField(default="", null=True, blank=True)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_of_order = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, null=True, blank=True)

    @property
    def get_order_total(self):
        items = self.orderitem_set.all()
        total = sum([item.get_total for item in items])
        total = round(total, 2)
        return total

    @property
    def get_item_count(self):
        items = self.orderitem_set.all()
        return sum([item.quantity for item in items])


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        total = round(total, 2)
        return total

# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
#     first_name = models.CharField(max_length=200, null=True)
#     last_name = models.CharField(max_length=200, null=True)
#     city = models.CharField(max_length=200, null=True)
#     street = models.CharField(max_length=200, null=True)
#     state = models.CharField(max_length=200, null=True)
#     zipcode = models.BigIntegerField(null=True)
#
#



