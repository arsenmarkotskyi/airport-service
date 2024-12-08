from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


from airport.models import Crew, Airplane, AirplaneType, Flight, Route, Airport, Ticket, Order
from airport.serializers import CrewSerializer, AirplaneSerializer, AirplaneTypeSerializer, FlightSerializer, \
    RouteSerializer, AirportSerializer, TicketSerializer, OrderSerializer, AirplaneListSerializer, RouteListSerializer, \
    FlightListSerializer, OrderListSerializer, TicketListSerializer, FlightDetailSerializer


class CrewViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirplaneViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Airplane.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return AirplaneListSerializer
        return AirplaneSerializer



class AirplaneTypeViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class FlightViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Flight.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return FlightListSerializer
        if self.action == 'retrieve':
            return FlightDetailSerializer
        return FlightSerializer


class RouteViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Route.objects.all().select_related('source', "destination")

    def get_serializer_class(self):
        if self.action in  ('list', 'retrieve'):
            return RouteListSerializer
        return RouteSerializer


class AirportViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class TicketViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TicketListSerializer
        return TicketSerializer


class OrderViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OrderListSerializer
        return OrderSerializer


