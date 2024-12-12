from django.db.models import Count, ExpressionWrapper, F, IntegerField, Q
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
    queryset = Airplane.objects.all().select_related("airplane_type")

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
    queryset = Flight.objects.all().select_related(
        'route__source', 'route__destination', 'airplane'
    )


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
    queryset = Route.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = (
                queryset
                .select_related('source', 'destination')
                .annotate(
                    tickets_available=ExpressionWrapper(
                        F("flights__airplane__rows") * F("flights__airplane__seats_in_row") - Count(
                            "flights__tickets",
                            filter=Q(flights__tickets__isnull=False)
                        ),
                        output_field=IntegerField()
                    )

                ).order_by("id")
            )
        return queryset

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


# class TicketViewSet(mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     GenericViewSet):
#     queryset = Ticket.objects.all()
#
#     def get_serializer_class(self):
#         if self.action in ('list', 'retrieve'):
#             return TicketListSerializer
#         return TicketSerializer


class OrderViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Order.objects.all().prefetch_related(
        'tickets__flight__airplane',
        'tickets__flight__route__source',
        'tickets__flight__route__destination',
        'tickets__flight__route__source__airport',
        'tickets__flight__route__destination__airport'
    )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OrderListSerializer
        return OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




