from django.contrib import admin

from airport.models import (
    Crew, Airplane,
    AirplaneType, Flight,
    Route, Airport,
    Ticket, Order
)

admin.site.register(Crew)
admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Flight)
admin.site.register(Route)
admin.site.register(Airport)
admin.site.register(Ticket)
admin.site.register(Order)
