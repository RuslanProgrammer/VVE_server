from django.urls import path
from rest_framework.routers import DefaultRouter

from mainApp.views import *

router = DefaultRouter()
router.register(r'shops', ShopViewSet, basename='shop')
router.register(r'administrators', AdministratorViewSet, basename='administrator')
router.register(r'workers', WorkerViewSet, basename='worker')
router.register(r'checkouts', CheckoutViewSet, basename='checkout')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'customerHistory', CustomerHistoryViewSet, basename='customerHistory')
router.register(r'checkoutHistory', CheckoutHistoryViewSet, basename='checkoutHistory')
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = router.urls

urlpatterns += [
    path('shops/getFreeWorkers/<int:pk>', WorkerFreeListView.as_view()),
    path('shops/getFreeCheckouts/<int:pk>', CheckoutsFreeOfShopListView.as_view()),
    path('shops/getCheckouts/<int:pk>/', CheckoutsOfShopListView.as_view()),
    path('customers/customerHistory/<int:pk>', HistoryOfCustomerListView.as_view()),
    path('customers/reservations/<int:pk>', ReservationsOfCustomerListView.as_view()),
    path('shops/customerHistory/<int:pk>', HistoryOfShopListView.as_view()),
    path('shops/Customers/<int:pk>', CustomersOfShopListView.as_view()),
    path('checkouts/getHistory/<int:pk>', HistoryOfCheckoutListView.as_view()),
    path('checkouts/updateMaxLoad/<int:pk>', UpdateMaxLoadOfCheckoutListView.as_view()),
    path('checkouts/getInfo/<int:pk>/', CheckoutsInfoOfShopListView.as_view()),
    path('checkouts/getCustomers/<int:pk>', CheckoutsICustomersListView.as_view()),
    path('checkoutsHistory/simulate', SimulateListView.as_view()),
    path('shops/getSituation/<int:pk>', CommonInfoOfShopListView.as_view()),
    path('shops/getTime/<int:pk>', BetterTimeToVisitShopListView.as_view()),
    path('shops/getAllTime', BetterTimeToVisitAllShopListView.as_view()),
    path('checkouts/changeWorker/<int:pk>', ChangeWorkerOfCheckoutListView.as_view()),
    path('checkouts/changeAnyWorker/<int:pk>', ChangeAnyWorkerOfCheckoutListView.as_view()),
    path('checkouts/rebalance_by_shop/<int:pk>', RebalanceByShopListView.as_view()),
    path('workers/getFreeWorkersAndCurrentByCheckout/<int:pk>', GetWorkerOfCheckoutByCheckoutListView.as_view()),
    path('checkouts/SimulateVisitors/<int:pk>', SimulateVisitors.as_view()),

    path('backups/create/', CreateBackup.as_view()),
    path('backups/get/', GetBackups.as_view()),
    path('backups/restore/<int:pk>', RestoreBackup.as_view()),
    path('backups/restore_last/', RestoreLastBackup.as_view()),
]
