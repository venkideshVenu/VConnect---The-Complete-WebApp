from django.db import models
from django.utils import timezone
from django.conf import settings

class Station(models.Model):
    station_name = models.CharField(max_length=100, default="")
    station_latitude = models.FloatField(null=True)
    station_longitude = models.FloatField(null=True)
    image = models.ImageField(upload_to='locations/', default='locations/location.png', blank=True)

    def __str__(self):
        return self.station_name

    @property
    def number_of_bikes(self):
        available_bikes = self.bike_set.all().filter(in_use=False, is_faulty=False)
        return available_bikes.count()

class Bike(models.Model):
    name = models.CharField(max_length=100,default='no_name')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='bike_set')
    in_use = models.BooleanField(default=False)
    is_faulty = models.BooleanField(default=False)
    image = models.ImageField(upload_to='bikeimage/', default='bikeshare/default.png', blank=True)


    class Meta:
        verbose_name_plural = 'Bikes'

    def current_usage(self):
        return "In Use" if self.in_use else "Free"

    def condition(self):
        return "Faulty" if self.is_faulty else "Good"

# bikeshare/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class BikeShareProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bikeshare_profile'
    )
    role = models.CharField(
        max_length=10,
        choices=[
            ('Customer', 'Customer'),
            ('Operator', 'Operator'),
            ('Manager', 'Manager'),
        ],
        null=True,
        blank=True
    )
    hires_in_progress = models.IntegerField(default=0)
    wallet_balance = models.FloatField(default=0.00)
    amount_owed = models.FloatField(default=0.00)
    

    def __str__(self):
        return f"{self.user.username}'s BikeShare Profile"

    class Meta:
        verbose_name = 'BikeShare Profile'
        verbose_name_plural = 'BikeShare Profiles'

# bikeshare/admin.py


class Order(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='startstation')
    end_station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(default=timezone.now)
    due_amount = models.FloatField(default=0.00)
    fix_amount = models.FloatField(default=0.00)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Order ID: {self.pk} - Customer: {self.user.username} - Bike ID: {self.bike.pk}"
