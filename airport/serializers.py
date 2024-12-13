from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import Crew, Airplane, AirplaneType, Flight, Route, Airport, Ticket, Order


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_name = serializers.CharField(source="airplane_type.name", read_only=True)
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_name")



class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "departure_time", "arrival_time", "route", "airplane")


class FlightListSerializer(serializers.ModelSerializer):
    airplane_name = serializers.CharField(source="airplane.name", read_only=True)
    route_from = serializers.CharField(source="route.source.name", read_only=True)
    route_to = serializers.CharField(source="route.destination.closet_big_city", read_only=True)
    class Meta:
        model = Flight
        fields = ("id", "departure_time", "arrival_time", "airplane_name", "route_from", "route_to")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "distance", "source", "destination")


class RouteListSerializer(serializers.ModelSerializer):
    move_from = serializers.CharField(source="source.name", read_only=True)
    move_to = serializers.CharField(source="destination.closet_big_city", read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Route
        fields = ("id", "distance", "move_from", "move_to", "tickets_available")



class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError
        )

        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")


class TicketListSerializer(serializers.ModelSerializer):
    departure = serializers.CharField(source="flight.departure_time", read_only=True)
    arrival = serializers.CharField(source="flight.arrival_time", read_only=True)
    created_at = serializers.DateTimeField(source="order.created_time", read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "departure", "arrival", "created_at")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ("id", "created_time", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=True, allow_empty=False)
    class Meta:
        model = Order
        fields = ("id", "created_time", "tickets")


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer(read_only=True)
    airplane = AirplaneListSerializer(read_only=True)





