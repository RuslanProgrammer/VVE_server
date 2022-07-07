from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import CustomerTokenObtainPairSerializer, AdministratorTokenObtainPairSerializer, \
    AdministratorRegisterSerializer, CustomerRegisterSerializer, WorkerRegisterSerializer, \
    WorkerTokenObtainPairSerializer
from mainApp.models import Administrator, Customer, Worker


class AdministratorObtainTokenPairView(TokenObtainPairView):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorTokenObtainPairSerializer
    # permission_classes = (AllowAny,)


class AdministratorRegisterView(CreateAPIView):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorRegisterSerializer
    permission_classes = (AllowAny,)


class CustomerObtainTokenPairView(TokenObtainPairView):
    queryset = Customer.objects.all()
    serializer_class = CustomerTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class CustomerRegisterView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer
    permission_classes = (AllowAny,)


class WorkerObtainTokenPairView(TokenObtainPairView):
    queryset = Worker.objects.all()
    serializer_class = WorkerTokenObtainPairSerializer
    # permission_classes = (AllowAny,)


class WorkerRegisterView(generics.CreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerRegisterSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTTokenUserAuthentication]
