from django.urls import path, include
from rest_framework import routers

from airport.views import CrewViewSet, AirplaneViewSet, AirplaneTypeViewSet, FlightViewSet, RouteViewSet, \
    AirportViewSet, OrderViewSet, TicketViewSet

# TicketViewSet

app_name = 'airport'

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("flights", FlightViewSet)
router.register("routes", RouteViewSet)
router.register("airports", AirportViewSet)
router.register("tickets", TicketViewSet)
router.register("orders", OrderViewSet)


urlpatterns = [path("", include(router.urls))]
