from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import timezone
import datetime
# Create your models here.

DELIVERY_STATUS = (
    ('W', 'WAITING'),
    ('I', 'IN_PROCESS'),
    ('D', 'DELIVERED')
)


class Customer(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    profile_picture = models.FileField(upload_to='media',  null=True, default=None)


class Driver(models.Model):
    account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20)
    active = models.BooleanField(default=False)
    profile_picture = models.FileField(upload_to='media',  null=True, default=None)
    description = models.TextField(default="Service nziza niyo ntego.")
    has_profile = models.BooleanField(default=False)

    def how_many_cars(self):
        vehicles = Vehicle.objects.filter(driver=self)
        return vehicles.count()

    def calculate_capacity(self):
        vehicles = Vehicle.objects.filter(driver=self)
        kilograms = 0
        for vehicle in vehicles:
            if vehicle.capacity is not None:
                kilograms += vehicle.capacity

        if 500 > kilograms > 1:
            return f"{kilograms} Kg"
        elif kilograms > 500:
            return f"{kilograms/1000} Ton"
        return "Ntacyatangajwe"

    def get_assigned_deliveries(self):
        deliveries = Delivery.objects.filter(driver=self, status='I').order_by('-departure_date_time')
        return deliveries


class Delivery(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=100, unique=True)
    status = models.CharField(choices=DELIVERY_STATUS, default="W",  max_length=11)
    date = models.DateTimeField(auto_now_add=True)
    departure_date_time = models.DateTimeField()
    arrival_date_time = models.DateTimeField()
    kilograms = models.IntegerField(default=1)
    destination = models.CharField(max_length=100, null=False)
    origin = models.CharField(max_length=100, null=False)
    price = models.IntegerField(default=500)

    def check_if_time_exhausted(self):
        today = timezone.now()
        time_difference = (self.departure_date_time - today).total_seconds()
        days = time_difference / (60 * 60 * 24)
        if days < 0:
            return True
        else:
            return False

    def date_printed(self):
        date = datetime.datetime.now()
        return date

    def show_kilograms(self):
        if self.kilograms > 500:
            return f"{self.kilograms/1000} Ton"
        else:
            return f"{self.kilograms} Kg"

    def get_remaining_time(self):
        today = timezone.now()
        time_difference = (self.departure_date_time - today).total_seconds()
        days = time_difference / (60 * 60 * 24)
        print(days)
        if days == 1:
            return "Uyumunsi"
        elif days > 7:
            return "Icyumweru kirenga"
        elif days < 0:
            return "Igihe cyararenze"
        elif days < 7:
            return f"Iminsi {int(days)}"

    def save(self, *args, **kwargs):

        if len(self.number) > 0:
            pass
        else:
            pk = Delivery.objects.all().count()
            self.number = f"{get_random_string(8).upper()}-{pk}"
        super(Delivery, self).save(*args, **kwargs)


class DriverWaitingList(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)


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

