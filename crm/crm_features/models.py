# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Chatroom(models.Model):
    room_name = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'chatroom'

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'customers'


class Message(models.Model):
    room = models.ForeignKey(Chatroom, models.DO_NOTHING, blank=True, null=True)
    sender = models.CharField(max_length=50)
    content = models.TextField()
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'message'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    transaction_id = models.IntegerField()
    date = models.DateField()
    product_category = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    units_sold = models.IntegerField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'products'


class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sale_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'sales'
