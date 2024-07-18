from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Bike, BikeRental
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import BikeRentalSerializer, BikeSerializer, RentalHistorySerializer


class BikesListCreateView(generics.ListCreateAPIView):
    serializer_class = BikeSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Bike.objects.all()
        status = self.request.query_params.get('status', None)
        if status:
            return self.queryset.filter(status=status)
        return self.queryset


class AvailableBikesListView(generics.ListAPIView):
    serializer_class = BikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Bike.objects.filter(status='available')


class BikeRentalViewSet(viewsets.ViewSet):
    def create(self, request):
        if BikeRental.objects.filter(user=request.user, is_active=True).exists():
            return Response({'error': 'You already have an active bike rental.'}, status=status.HTTP_400_BAD_REQUEST)

        bike_id = request.data.get('bike_id')
        try:
            bike = Bike.objects.get(id=bike_id, is_available=True)
        except Bike.DoesNotExist:
            return Response({'error': 'Bike not available or not found.'}, status=status.HTTP_400_BAD_REQUEST)

        bike_rental = BikeRental.objects.create(user=request.user, bike=bike)
        bike.is_available = False
        bike.save()

        serializer = BikeRentalSerializer(bike_rental)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def end_rental(self, request):
        try:
            bike_rental = BikeRental.objects.get(user=request.user, is_active=True)
        except BikeRental.DoesNotExist:
            return Response({'error': 'No active rental found.'}, status=status.HTTP_400_BAD_REQUEST)

        bike_rental.rental_end_time = timezone.now()
        bike_rental.rental_cost = bike_rental.calculate_rental_cost()
        bike_rental.is_active = False
        bike_rental.save()
        bike_rental.bike.is_available = True
        bike_rental.bike.save()

        serializer = BikeRentalSerializer(bike_rental)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RentalHistoryView(generics.ListAPIView):
    serializer_class = RentalHistorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return BikeRental.objects.filter(user=self.request.user)
