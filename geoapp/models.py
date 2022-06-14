from django.db import models

# Create your models here.

class Measurement(models.Model):
    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Distance from {self.location} to {self.destination} is {self.distance}kms"
 

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    desc = models.TextField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return str(self.name)