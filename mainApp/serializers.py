from rest_framework import serializers

from mainApp.models import Shop, Administrator, Worker, Checkout, Customer, CustomerHistory, CheckoutHistory, \
    Reservation


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'email', 'open_time', 'close_time', 'url', 'commonWaitingTime', 'image', 'created_at',
                  'updated_at')


class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = ('id', 'name', 'surname', 'email', 'shop')


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('id', 'name', 'surname', 'email', 'shop', 'created_at', 'updated_at')


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ('id', 'description', 'title', 'shop', 'worker', 'created_at', 'updated_at')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'surname', 'email')


class CustomerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerHistory
        fields = ('id', 'shop', 'start_visit', 'finish_visit', 'customer')


class CheckoutHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutHistory
        fields = ('id', 'checkout', 'time', 'max_load', 'cur_load')


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'shop', 'start_time', 'customer', 'created_at', 'updated_at')
