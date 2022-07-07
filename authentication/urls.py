from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import AdministratorObtainTokenPairView, AdministratorRegisterView, \
    CustomerObtainTokenPairView, CustomerRegisterView, WorkerObtainTokenPairView, WorkerRegisterView

urlpatterns = [
    path('administrator/login/', AdministratorObtainTokenPairView.as_view()),
    path('administrator/login/refresh/', TokenRefreshView.as_view()),
    path('administrator/register/', AdministratorRegisterView.as_view()),

    path('customer/login/', CustomerObtainTokenPairView.as_view()),
    path('customer/login/refresh/', TokenRefreshView.as_view()),
    path('customer/register/', CustomerRegisterView.as_view()),

    path('worker/login/', WorkerObtainTokenPairView.as_view()),
    path('worker/login/refresh/', TokenRefreshView.as_view()),
    path('worker/register/', WorkerRegisterView.as_view()),
]
