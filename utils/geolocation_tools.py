from geopy.geocoders import Nominatim
from typing import Dict, Any


geolocator = Nominatim(user_agent="GeoSort")

def locate(lat: float, lng: float) -> Dict[str, str]:
    location = geolocator.reverse("{:.6f},{:.6f}".format(lat, lng))
    return location.raw["address"]
