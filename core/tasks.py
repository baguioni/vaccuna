import googlemaps
from django.conf import settings

from core.models import AddressField


def GetCoordinates(address):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    return gmaps.geocode(address.get_formatted_address())

