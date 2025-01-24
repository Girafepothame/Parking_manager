from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Parking, Spot
from .serializers import ParkingSerializer, SpotSerializer

class ParkingViewSet(viewsets.ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer

class SpotViewSet(viewsets.ModelViewSet):
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer

    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        spot = self.get_object()
        try:
            spot.book()
            return Response({'status': 'Spot booked'})
        except ValueError as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=True, methods=['post'])
    def release(self, request, pk=None):
        spot = self.get_object()
        try:
            spot.release()
            return Response({'status': 'Spot released'})
        except ValueError as e:
            return Response({'error': str(e)}, status=400)
