from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
# Create your models here.

DELIVERY_STATUS = (
    ('W', 'WAITING'),
    ('I', 'IN_PROCESS'),
    ('D', 'DELIVERED')
)


class Customer(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)


class Driver(models.Model):
    account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20)
    active = models.BooleanField(default=False)
    # number_of_cars = models.IntegerField(default=1)
    # transport_capacity = models.IntegerField(default=1)
    description = models.TextField(default="Service nziza niyo ntego.")


class Delivery(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=100, unique=True)
    status = models.CharField(choices=DELIVERY_STATUS, max_length=11)
    date = models.DateTimeField(auto_now_add=True)
    departure_date_time = models.DateTimeField()
    arrival_date_time = models.DateTimeField()
    kilograms = models.IntegerField(default=1)
    destination = models.CharField(max_length=100, null=False)
    origin = models.CharField(max_length=100, null=False)
    price = models.IntegerField(default=500)

    def save(self, *args, **kwargs):
        self.status = "W"
        pk = Delivery.objects.all().count()
        self.number = f"{get_random_string(8).upper()}-{pk}"
        super(Delivery, self).save(*args, **kwargs)


class Product(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    kilograms = models.IntegerField(default=1)


class Vehicle(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    model = models.CharField(max_length=100)
    capacity = models.IntegerField(default=1)
    plate = models.CharField(max_length=12, default='RAA 000 A')

