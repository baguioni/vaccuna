import googlemaps
import gmplot
from vaccuna.settings import GOOGLE_MAPS_API_KEY
from django.core.files.base import ContentFile
from core.models import AddressField
from lgu.models import LocalGovernmentUnit
from vaccuna import settings


def get_coordinates(addresses):
    coordinates = []
    for address in addresses:
        obj = AddressField.objects.get(id=address['address'])
        coordinates.append((float(obj.latitude), float(obj.longitude)))
    coordinates_lats, coordinates_long = zip(*coordinates)

    return coordinates_lats, coordinates_long


def generate_registrant_markers_map(lgu):
    # Get address of registrants of LGU
    addresses = lgu.registrants.all().values('address',)
    coordinates_lats, coordinates_long = get_coordinates(addresses)
    gmap = gmplot.GoogleMapPlotter(float(lgu.latitude), float(lgu.longitude), 14, apikey=GOOGLE_MAPS_API_KEY)
    gmap.scatter(coordinates_lats, coordinates_long, color='cornflowerblue')

    vaccination_sites = lgu.vaccination_sites.all().values('address',)
    coordinates_lats, coordinates_long = get_coordinates(vaccination_sites)
    gmap.scatter(coordinates_lats, coordinates_long, color='red')

    html = ContentFile(gmap.get())
    lgu.registrant_map.save(f'{lgu.name}Map.html', html)


def generate_lgus_map():
    lgus = LocalGovernmentUnit.objects.all().values_list('name', flat=True)
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    coordinates = []

    for lgu in lgus:
        temp = gmaps.geocode(lgu + ' , Philippines')
        if temp:
            temp = temp[0]['geometry']['location']
            coordinates.append((temp['lat'], temp['lng']))
    coordinates_lats, coordinates_long = zip(*coordinates)
    gmap = gmplot.GoogleMapPlotter(12.8797, 121.774, 6, apikey=GOOGLE_MAPS_API_KEY)
    gmap.scatter(coordinates_lats, coordinates_long, color='cornflowerblue')
    gmap.draw('static/media/maps/landing.html')
