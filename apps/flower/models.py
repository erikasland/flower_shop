from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Flower(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Flower'

class Cart(models.Model):     
    user = models.OneToOneField(User, primary_key = True, related_name='cart')
    def __str__(self):
        return self.user.username

class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_details')
    flower = models.ForeignKey(Flower)
    flower_name = models.CharField(max_length=255)
    def __str__(self):
        return self.flower.name

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders')
    order = models.CharField(max_length=10000, default=None)
    def __str__(self):
        return self.user.username

