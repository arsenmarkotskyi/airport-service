from django.db.models import Count, ExpressionWrapper, F, IntegerField, Q
from django.utils.dateparse import parse_date
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet


from airport.models import Crew, Airplane, AirplaneType, Flight, Route, Airport, Ticket, Order
from airport.serializers import CrewSerializer, AirplaneSerializer, AirplaneTypeSerializer, FlightSerializer, \
    RouteSerializer, AirportSerializer, TicketSerializer, OrderSerializer, AirplaneListSerializer, RouteListSerializer, \
    FlightListSerializer, OrderListSerializer, TicketListSerializer, FlightDetailSerializer
from .permission import IsAdminOrIfAuthenticatedReadOnly


class CrewViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Airplane.objects.all().select_related("airplane_type")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class FlightViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Flight.objects.all().select_related(
        'route__source', 'route__destination', 'airplane'
    )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


    def get_serializer_class(self):
        if self.action == 'list':
            return FlightListSerializer
        if self.action == 'retrieve':
            return FlightDetailSerializer
        return FlightSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "departure_time",
                type={"type": "string", "format": "date-time"},
                description="Filter flight by departure_time "
                            "Use ISO 8601 format "
                            "(e.g., '2024-10-08').",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        departure_time = request.query_params.get("departure_time")
        if departure_time:
            date = parse_date(departure_time)
            if date:
                queryset = queryset.filter(departure_time__date=date)

        self.queryset = queryset
        return super().list(request, *args, **kwargs)


class RouteViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Route.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "route_from",
                type=str,
                description="Filter flight by town you route from "
                            "Use format like Zolochiv",
                required=False,
            ),
            OpenApiParameter(
                "destination",
                type=str,
                description="Filter flight by destination "
                            "Use format like Lviv",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        route_from = request.query_params.get("route_from")
        if route_from:
            queryset = queryset.filter(source__name__icontains=route_from)

        destination = request.query_params.get("destination")
        if destination:
            queryset = queryset.filter(destination__closet_big_city__icontains=destination)

        self.queryset = queryset
        return super().list(request, *args, **kwargs)


class AirportViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


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
    pagination_class = OrderPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OrderListSerializer
        return OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




