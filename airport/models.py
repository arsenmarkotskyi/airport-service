from django.db import models
from django.conf import settings



class Crew(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Airplane(models.Model):
    name = models.CharField(max_length=50)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey("AirplaneType", on_delete=models.CASCADE, related_name="airplanes")

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name

class AirplaneType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Flight(models.Model):
    route = models.ForeignKey("Route", on_delete=models.CASCADE, blank=True, related_name="flights")
    airplane = models.ForeignKey("Airplane", on_delete=models.CASCADE, blank=True, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ("-departure_time", "-arrival_time")

class Route(models.Model):
    source = models.ForeignKey("Airport", on_delete=models.CASCADE, blank=True, related_name="routes_as_source")
    destination = models.ForeignKey("Airport", on_delete=models.CASCADE, blank=True, related_name="routes_as_destination")
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} - {self.destination}"

class Airport(models.Model):
    name = models.CharField(max_length=50)
    closet_big_city = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE, blank=True, related_name="tickets")
    order = models.ForeignKey("Order", on_delete=models.CASCADE, blank=True, related_name="tickets")

    def __str__(self):
        return f"{self.row} - {self.seat} - {self.flight}"

    class Meta:
        unique_together = (("row", "seat", "flight"),)
        ordering = ("row", "seat")


class Order(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    class Meta:
        ordering = ("created_time",)