from django.contrib.auth import get_user_model
from django.urls import reverse

from airport.models import Flight, Route, Airport, Airplane
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from airport.serializers import RouteListSerializer

ROUTE_URL = reverse("airport:route-list")
FLIGHT_URL = reverse("airport:flight-list")


def sample_route(**params):
    defaults = {
        "distance": 90,
    }
    defaults.update(params)

    return Route.objects.create(**defaults)

def sample_airport(**params):
    defaults = {
        "name": "Test name",
        "closet_big_city": "Test city",
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


# def sample_airplane(**params):
#     defaults = {
#         "name": "Test airplane",
#     }
#     defaults.update(params)
#
#     return Airplane.objects.create(**defaults)


def sample_flight(**params):
    airplane = Airplane.objects.create(name="Test airplane")
    defaults = {
        "airplane": airplane,
        "departure_time": "2024-06-02 14:00:00",
        "arrival_time": "2024-06-03 14:00:00",
    }
    defaults.update(params)

    return Flight.objects.create(**defaults)


class UnauthenticatedMovieApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ROUTE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedMovieApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="test123"
        )
        self.client.force_authenticate(self.user)


    def test_route_list(self):
        sample_route()

        route_with_source = sample_route()

        airport_1 = Airport.objects.create(name="Test name")
        airport_2 = Airport.objects.create(name="Test name2")

        route_with_source.airports.add(airport_1, airport_2)

        response = self.client.get(ROUTE_URL)
        movies = Route.objects.all()
        serializer = RouteListSerializer(movies, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, serializer.data)

