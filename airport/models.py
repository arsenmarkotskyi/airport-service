from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError


class Crew(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        app_label = 'airport'

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

    class Meta:
        app_label = 'airport'

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name

class AirplaneType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'airport'

    def __str__(self):
        return self.name


class Flight(models.Model):
    route = models.ForeignKey("Route", on_delete=models.CASCADE, blank=True, related_name="flights")
    airplane = models.ForeignKey("Airplane", on_delete=models.CASCADE, blank=True, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ("-departure_time", "-arrival_time")
        app_label = 'airport'


    def __str__(self):
        return f"{self.departure_time} - {self.arrival_time}"

class Route(models.Model):
    source = models.ForeignKey("Airport", on_delete=models.CASCADE, blank=True, related_name="routes_as_source")
    destination = models.ForeignKey("Airport", on_delete=models.CASCADE, blank=True, related_name="routes_as_destination")
    distance = models.IntegerField()

    class Meta:
        app_label = 'airport'


    def clean(self):
        if self.source == self.destination:
            raise ValidationError("Source and destination airports must be different")

    def __str__(self):
        return f"{self.source.name} - {self.destination.closet_big_city}"

class Airport(models.Model):
    name = models.CharField(max_length=50)
    closet_big_city = models.CharField(max_length=50)

    class Meta:
        app_label = 'airport'


    def __str__(self):
        return f"{self.name} {self.closet_big_city}"

class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE, blank=True, related_name="tickets")
    order = models.ForeignKey("Order", on_delete=models.CASCADE, blank=True, related_name="tickets")

    class Meta:
        app_label = 'airport'



    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        if row is None or seat is None:
            raise error_to_raise({"row": "Row and seat must not be None"})

        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {count_attrs}))"
                    }
                )

    # def __str__(self):
    #     return f"{self.row} - {self.seat}"

    class Meta:
        unique_together = (("row", "seat", "flight"),)
        ordering = ("row", "seat", "flight")
        app_label = 'airport'



    def clean(self):
        if not (1 <= self.seat <= self.flight.airplane.seats_in_row):
            raise ValidationError({
                "seat": f"seat must be in range [1, {self.flight.airplane.seats_in_row}]"
            })


    def save(self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )

class Order(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    class Meta:
        ordering = ("created_time",)
        app_label = 'airport'


    def __str__(self):
        return f"{self.created_time}"