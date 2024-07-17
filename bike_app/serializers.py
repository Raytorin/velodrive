from rest_framework import serializers
# from .models import Bike, Rental
from .models import Bike, BikeRental
from django.utils import timezone


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ('id', 'name', 'status')


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'


class BikeRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeRental
        fields = '__all__'


class RentalHistorySerializer(serializers.ModelSerializer):
    bike = BikeSerializer(read_only=True)
    cost = serializers.SerializerMethodField()

    class Meta:
        model = BikeRental
        fields = ('id', 'bike', 'start_time', 'end_time', 'cost')

    def get_cost(self, obj):
        return obj.calculated_cost()
