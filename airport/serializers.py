from rest_framework import serializers

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
    route_from = serializers.CharField(source="route.source", read_only=True)
    route_to = serializers.CharField(source="route.destination", read_only=True)
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
    class Meta:
        model = Route
        fields = ("id", "distance", "move_from", "move_to")



class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Order
        fields = ("id", "created_time", "user")


class OrderListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = Order
        fields = ("id", "created_time", "user_name")


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer(read_only=True)
    airplane = AirplaneListSerializer(read_only=True)





