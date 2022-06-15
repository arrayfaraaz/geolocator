from django.shortcuts import render, HttpResponse
from .forms import MeasurementForm
from .models import Measurement, Contact
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import folium
from .utils import get_center_coordinates, get_zoom
from django.contrib import messages
from datetime import datetime
from django.core.mail import send_mail


# Create your views here.
def calculate_distance(request):

    distance = None
    location = None
    destination = None
    geolocator = Nominatim(user_agent="geoapp")
    

    form = MeasurementForm(request.POST or None)

    # Initial folium map

    initial_map_lat = 26.449923
    initial_map_lon = 80.331871
    initial_map_location = geolocator.geocode("Kanpur")

    m = folium.Map(width=900, height=700, location=[initial_map_lat, initial_map_lon], zoom_start=8)

    # Location marker
    folium.Marker([initial_map_lat, initial_map_lon], tooltip='Click here for more', popup=initial_map_location,
     icon=folium.Icon(color='blue')).add_to(m)

    

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

        
        # Folium map modifications
        m = folium.Map(width=1000, height=700, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon),
         zoom_start=get_zoom(distance))

        # Location marker
        folium.Marker([l_lat, l_lon], tooltip="Click here for more", popup=location,
         icon=folium.Icon(color="blue")).add_to(m)

        # Destination marker
        folium.Marker([d_lat, d_lon], tooltip="Click here for more", popup=destination,
         icon=folium.Icon(color="destination", icon="cloud")).add_to(m) 

        # Line between Location and Destination
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color="blue")
        m.add_child(line)


        instance.location = location
        instance.destination = destination
        instance.distance = distance
        instance.save()
        form = MeasurementForm()
        messages.success(request, f"Distance from {location} to {destination} is {distance}kms")

    m = m._repr_html_()

    context = {
            'form':form,
            'distance': distance,
            'location': location,
            'destination': destination,
            'map': m,
        }

    return render(request, "index.html", context)



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, desc=desc, date=datetime.today())
        contact.save()

        messages.success(request, "Your response has been submitted")

        send_mail(
            "This is an automated mail sent directly from the server.",
            f"Hello {name},\n\n We are so glad to hear from you and we are here to help you with everything we can. As you mentioned the reason '{desc}' we want you to elaborate a little so that we can help you with specific approach. Feel free to reply to this Email.\n\n\n\n\n Thanks\n GeoLocator Team ",
            "your_email",
            ["to_email"],
            fail_silently=False
        )




    return render(request, "contactus.html")


