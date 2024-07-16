from rest_framework import serializers
from .models import Bike, Rental
from django.utils import timezone


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ('id', 'name', 'status')


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ('id', 'user', 'bike', 'start_time', 'end_time', 'cost')

    cost = serializers.SerializerMethodField()

    def get_cost(self, obj):
        return obj.calculated_cost()

    def create(self, validated_data):
        bike = validated_data.get('bike')
        if bike.status != 'available':
            raise serializers.ValidationError('This bike is not available for rent.')
        bike.status = 'rented'
        bike.save()
        rental = Rental.objects.create(**validated_data)
        return rental


class ReturnRentalSerializer(serializers.ModelSerializer):
    cost = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = ('end_time', 'cost')

    def get_cost(self, obj):
        return obj.calculated_cost()

    def update(self, instance, validated_data):
        instance.end_time = validated_data.get('end_time', timezone.now())
        instance.save()

        bike = instance.bike
        bike.status = 'available'
        bike.save()

        return instance


class RentalHistorySerializer(serializers.ModelSerializer):
    bike = BikeSerializer(read_only=True)
    cost = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = ('id', 'bike', 'start_time', 'end_time', 'cost')

    def get_cost(self, obj):
        return obj.calculated_cost()
