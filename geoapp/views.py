from turtle import width
from django.shortcuts import render
from .forms import MeasurementForm
from .models import Measurement
from geopy.geocoders import Nominatim
from geopy.distance import geodesic, great_circle
import folium


# Create your views here.
def calculate_distance(request):

    distance = None
    location = None
    destination = None
    geolocator = Nominatim(user_agent="geoapp")
    

    form = MeasurementForm(request.POST or None)

    # Initial folium map

    initial_map_lat = 53.480759
    initial_map_lon = -2.242631

    m = folium.Map(width=1000, height=700, location=[initial_map_lat, initial_map_lon])

    

    if form.is_valid():
        instance = form.save(commit=False)
        location_ = form.cleaned_data.get('location')
        location = geolocator.geocode(location_)

        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)

        # Location Coordinates
        l_lat = location.latitude
        l_lon = location.longitude
        pointA = (l_lat, l_lon)

        # Destination Coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB = (d_lat, d_lon)

        
        # Distance Calculation
        distance = round(great_circle(pointA, pointB).km, 2)

        instance.location = location
        instance.destination = destination
        instance.distance = distance
        instance.save()

    m = m._repr_html_()

    context = {
            'form':form,
            'distance': distance,
            'location': location,
            'destination': destination,
            'map': m,
        }

    

    return render(request, "index.html", context)