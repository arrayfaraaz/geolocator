from django.urls import path
from geoapp import views

app_name = "geoapp"

urlpatterns = [
    path('', views.calculate_distance, name="calculate_distance"),
    path("contactus/", views.contact, name="contact")
]

