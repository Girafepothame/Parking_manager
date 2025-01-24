from django.db import models
from django.utils import timezone

class Parking(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Spot(models.Model):
    parking = models.ForeignKey(Parking, related_name='spots', on_delete=models.CASCADE)
    spot_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('libre', 'Libre'), ('occupée', 'Occupée')], default='libre')

    class Meta:
        unique_together = ('parking', 'spot_number')

    def __str__(self):
        return f"Spot {self.spot_number} - {self.parking.name}"

    def book(self):
        if self.status == 'libre':
            self.status = 'occupée'
            self.save()
        else:
            raise ValueError("Spot already occupied")

    def release(self):
        if self.status == 'occupée':
            self.status = 'libre'
            self.save()
        else:
            raise ValueError("Spot already free")
