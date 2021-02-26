import googlemaps
import gmplot
from vaccuna.settings import GOOGLE_MAPS_API_KEY
from django.core.files.base import ContentFile
from core.models import AddressField


def generate_registrant_markers_map(lgu):
    # Get address of registrants of LGU
    addresses = lgu.registrants.all().values('address',)
    coordinates = []
    for address in addresses:
        obj = AddressField.objects.get(id=address['address'])
        coordinates.append((float(obj.latitude), float(obj.longitude)))
    coordinates_lats, coordinates_long = zip(*coordinates)
    gmap = gmplot.GoogleMapPlotter(float(lgu.latitude), float(lgu.longitude), 14, apikey=GOOGLE_MAPS_API_KEY)
    gmap.scatter(coordinates_lats, coordinates_long, color='cornflowerblue')
    # import ipdb; ipdb.set_trace()
    html = ContentFile(gmap.get())
    lgu.registrant_map.save(f'{lgu.name}Map.html', html)


