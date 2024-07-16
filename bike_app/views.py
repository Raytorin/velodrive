from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Bike, Rental
from .serializers import BikeSerializer, ReturnRentalSerializer, RentalHistorySerializer, RentalSerializer
from django.utils import timezone


class AvailableBikesListView(generics.ListAPIView):
    serializer_class = BikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Bike.objects.filter(status='available')


class RentBikeView(generics.CreateAPIView):
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if Rental.objects.filters(user=user, end_time__isnull=True).exists():
            raise ValidationError('You already have an ongoing rental.')

        bike = serializer.validated_data['bike']
        if bike.status != 'available':
            raise ValidationError('This bike is not available for rent.')

        serializer.save(user=user)
        bike.status = 'rented'
        bike.save()


class ReturnBikeView(generics.UpdateAPIView):
    serializer_class = ReturnRentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Rental.objects.filter(user=user, end_time__isnull=True)

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.end_time = timezone.now()
        instance.save()


class RentalHistoryView(generics.ListAPIView):
    serializer_class = RentalHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Rental.objects.filter(user=user).order_by('-start_time')
