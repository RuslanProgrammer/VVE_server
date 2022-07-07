from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from mainApp.models import Administrator, Customer, Worker
from mainApp.serializers import AdministratorSerializer, CustomerSerializer, WorkerSerializer


class AdministratorTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        try:
            request = self.context["request"]
            user = Administrator.objects.filter(email=request.data['email']).first()
            if user.check_password(request.data['password']):
                self.user = user

            refresh = self.get_token(self.user)

            data = {'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': AdministratorSerializer(user).data,
                    'role': 'Administrator'
                    }

            return data

        except Exception:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )


class AdministratorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = ('email', 'password', 'name', 'surname', 'shop')

    def create(self, validated_data):
        user = Administrator.objects.create_administrator(
            email=validated_data['email'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            shop=validated_data['shop'].id,
            password=validated_data['password'],
        )
        return user


class CustomerTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        try:
            request = self.context["request"]
        except KeyError:
            pass

        try:
            request_data = request.data
            print(request_data)
            user = Customer.objects.filter(email=request_data['email']).first()
            if user.check_password(request_data['password']):
                self.user = user
            refresh = self.get_token(self.user)
            data = {'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': 'Customer',
                    'user': CustomerSerializer(user).data}

            return data

        except Exception:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('email', 'password', 'name', 'surname')

    def create(self, validated_data):
        user = Customer.objects.create_customer(
            email=validated_data['email'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            password=validated_data['password'],
        )
        return user


class WorkerTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        try:
            request = self.context["request"]
        except KeyError:
            pass

        try:
            request_data = request.data
            user = Worker.objects.filter(email=request_data['email']).first()
            if user.check_password(request_data['password']):
                self.user = user

            refresh = self.get_token(self.user)

            data = {'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': 'Worker',
                    'user': WorkerSerializer(user).data}

            return data

        except:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )


class WorkerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('email', 'password', 'name', 'surname', 'shop')

    def create(self, validated_data):
        user = Worker.objects.create_worker(
            email=validated_data['email'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            shop=validated_data['shop'].id,
            password=validated_data['password'],
        )
        return user
