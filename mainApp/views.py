import datetime
import json
import os
import random
import time
from datetime import datetime as dt

from django.core import management
from django.utils.timezone import utc
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from mainApp.models import Shop, Administrator, Worker, Checkout, Customer, CustomerHistory, CheckoutHistory, \
    Reservation
from mainApp.serializers import ShopSerializer, CheckoutSerializer, \
    CustomerHistorySerializer, CheckoutHistorySerializer, ReservationSerializer, CustomerSerializer, \
    AdministratorSerializer, WorkerSerializer


class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()

    # permission_classes = [IsAuthenticated]


class AdministratorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdministratorSerializer
    queryset = Administrator.objects.all()

    # authentication_classes = [JWTTokenUserAuthentication]
    # permission_classes = [IsAuthenticated]


class WorkerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()

    # authentication_classes = [JWTTokenUserAuthentication]
    # permission_classes = [IsAuthenticated]


class CheckoutViewSet(viewsets.ModelViewSet):
    serializer_class = CheckoutSerializer
    queryset = Checkout.objects.all()

    # authentication_classes = [JWTTokenUserAuthentication]
    # permission_classes = [IsAuthenticated]


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    #
    # authentication_classes = [JWTTokenUserAuthentication]
    # permission_classes = [IsAuthenticated]


class CustomerHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerHistorySerializer
    queryset = CustomerHistory.objects.all()

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]


class CheckoutHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = CheckoutHistorySerializer
    queryset = CheckoutHistory.objects.all()

    # authentication_classes = [JWTTokenUserAuthentication]
    # permission_classes = [IsAuthenticated]


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    # authentication_classes = [JWTTokenUserAuthentication]
    # permission_classes = [IsAuthenticated]


class CheckoutsOfShopListView(APIView):

    def get(self, request, pk):
        checkouts = Checkout.objects.filter(shop=pk)
        return Response(CheckoutSerializer(checkouts, many=True).data)


class CheckoutsFreeOfShopListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        checkouts_id = [x.id for x in Checkout.objects.filter(shop=pk)]
        print(checkouts_id)
        history = []
        for x in range(len(checkouts_id)):
            history.append(
                CheckoutHistory.objects.filter(checkout__in=checkouts_id).filter(checkout=checkouts_id[x]).order_by(
                    'id').last())

        res = list(set([(x.checkout_id, x.max_load - x.cur_load) for x in history if x.max_load - x.cur_load > 0]))
        print(res)

        content = {
            'Free checkouts': json.dumps(res),
        }
        return Response(content)


class SimulateListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        for _ in range(10000):
            checkout1 = CheckoutHistory.objects.filter(id=1).order_by('id').last()
            checkout2 = CheckoutHistory.objects.filter(id=2).order_by('id').last()
            c1 = CheckoutHistory.objects.create(checkout_id=1,
                                                max_load=max(0, checkout1.max_load + random.randint(-2, 2)),
                                                cur_load=max(0, checkout1.cur_load + random.randint(-2, 2)))
            c2 = CheckoutHistory.objects.create(checkout_id=2,
                                                max_load=max(0, checkout2.max_load + random.randint(-2, 2)),
                                                cur_load=max(0, checkout2.cur_load + random.randint(-2, 2)))
            c1.save()
            c2.save()
            time.sleep(0.5)


class CheckoutsInfoOfShopListView(APIView):
    # authentication_classes = [JWTTokenUserAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        checkout_history = CheckoutHistory.objects.filter(checkout=pk).order_by('id').last()
        checkout = Checkout.objects.filter(id=pk).first()
        if checkout_history is None:
            CheckoutHistory.objects.create(checkout_id=pk, cur_load=0)
            checkout_history = CheckoutHistory.objects.filter(checkout=pk).order_by('id').last()
        content = {
            'checkout_id': checkout.id,
            'shop': checkout.shop_id,
            'worker': checkout.worker_id,
            'max_load': checkout_history.max_load,
            'cur_load': checkout_history.cur_load,
            'last_update': checkout_history.time,
        }

        return Response(content)


class CheckoutsICustomersListView(APIView):

    def get(self, request, pk):
        checkout_history = CheckoutHistory.objects.filter(checkout=pk).order_by('id').last()
        if checkout_history is None:
            return Response(0)

        return Response(checkout_history.cur_load)



class HistoryOfCustomerListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        customer_history = CustomerHistory.objects.filter(customer=pk)
        content = {
            'User`s History Id': json.dumps([x.id for x in customer_history]),
        }
        return Response(content)


class HistoryOfShopListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        customer_history = CustomerHistory.objects.filter(shop=pk)
        content = {
            'Shop`s History Id': json.dumps([x.id for x in customer_history]),
        }
        return Response(content)


class WorkersOfShopListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        workers = Worker.objects.filter(shop=pk)
        content = {
            'Shop`s Workers Id': json.dumps([x.id for x in workers]),
        }
        return Response(content)


class CustomersOfShopListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        customers_history = CustomerHistory.objects.filter(shop=pk)

        uni_customers = list(set([x.customer_id for x in customers_history]))
        content = {
            'Shop`s Customer`s Id': json.dumps(uni_customers),
        }
        return Response(content)


class WorkerFreeListView(APIView):
    # authentication_classes = [JWTTokenUserAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        checkouts = Checkout.objects.filter(shop=pk)
        workers = Worker.objects.filter(shop=pk)
        working_workers = [x.worker for x in checkouts]
        free_workers = list(set(workers) - set(working_workers))
        return Response(WorkerSerializer(free_workers, many=True).data)


class HistoryOfCheckoutListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        checkout_history = CheckoutHistory.objects.filter(checkout_id=pk)
        content = {
            'Checkout`s History Id': json.dumps([x.id for x in checkout_history]),
        }
        return Response(content)


class UpdateMaxLoadOfCheckoutListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        checkout_history = CheckoutHistory.objects.filter(checkout_id=pk).order_by('id').last()
        print(checkout_history.id)
        checkout_history.max_load = int(request.data['max_load'])
        checkout_history.save()
        return Response({
            "success": f"Checkout`s Max Load was changed to {int(request.data['max_load'])} successfully"
        })


class GetFuturePredictionListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(get, request, pk):
        checkout_history = CheckoutHistory.objects.filter(checkout_id=pk).order_by('id').last()
        print(checkout_history.id)
        checkout_history.max_load = int(request.data['max_load'])
        checkout_history.save()
        return Response({
            "success": f"Checkout`s Max Load was changed to {int(request.data['max_load'])} successfully"
        })


class CommonInfoOfShopListView(APIView):

    def get(self, request, pk):

        checkouts_id = [x.id for x in Checkout.objects.filter(shop=pk)]

        history = []
        for x in range(len(checkouts_id)):
            history.append(
                CheckoutHistory.objects.filter(checkout__in=checkouts_id).filter(checkout=checkouts_id[x]).order_by(
                    'id').last())

        res = [[x.checkout.title, x.max_load - x.cur_load] for x in history if x is not None]
        content = {}
        for x in res:
            if x[1] < 0:
                content[x[0]] = - x[1]
        if not content:
            return Response({})

        return Response(content)


class SimulateVisitors(APIView):

    def get(self, request, pk):
        checkouts = Checkout.objects.filter(shop_id=pk)

        checkout = checkouts.last()
        CheckoutHistory.objects.create(checkout=checkout, max_load=3, cur_load=5)

        return Response()



class BetterTimeToVisitShopListView(APIView):

    def get(self, request, pk):

        checkouts_id = [x.id for x in Checkout.objects.filter(shop=pk)]

        history = []
        time_for_one_customer = 1.25
        for x in range(len(checkouts_id)):
            history.append(
                CheckoutHistory.objects.filter(checkout__in=checkouts_id).filter(checkout=checkouts_id[x]).order_by(
                    'id').last())
        add_time = 0
        for reservation in Reservation.objects.filter(shop=pk):
            if utc.localize(dt.now()) + datetime.timedelta(minutes=10) >= reservation.start_time > dt.now():
                add_time += 1

        if len(history) > 0:
            res = [[x.checkout, x.max_load - x.cur_load] for x in history if x is not None]

            if len(res) >= 1:
                return Response(
                    f'Not now. About {time_for_one_customer + ((res[0][1] + add_time) * time_for_one_customer)} minutes later')

        return Response('Checkouts are clear. Youre are welcome!')


class BetterTimeToVisitAllShopListView(APIView):

    def get(self, request):

        shops = Shop.objects.all()
        content = dict()
        for shop in shops:
            pk = shop.id
            checkouts_id = [x.id for x in Checkout.objects.filter(shop=pk)]

            history = []
            time_for_one_customer = 1.25
            for x in range(len(checkouts_id)):
                history.append(
                    CheckoutHistory.objects.filter(checkout__in=checkouts_id).filter(checkout=checkouts_id[x]).order_by(
                        'id').last())
            add_time = 0
            for reservation in Reservation.objects.filter(shop=shop):
                if utc.localize(dt.now()) + datetime.timedelta(minutes=10) >= reservation.start_time > utc.localize(
                        dt.now()):
                    add_time += 1
            if len(history) > 0:
                res = [[x.checkout, x.max_load - x.cur_load] for x in history if x is not None]

                if len(res) >= 1:
                    content[
                        pk] = f'Not now. About {time_for_one_customer + ((- res[0][1] + add_time) * time_for_one_customer)} minutes later'
                elif add_time > 0:
                    content[
                        pk] = f'Not now. About {time_for_one_customer + (add_time * time_for_one_customer)} minutes later'
                else:
                    content[pk] = 'Checkouts are clear. Youre are welcome!'
            elif add_time > 0:
                content[
                    pk] = f'Not now. About {time_for_one_customer + (add_time * time_for_one_customer)} minutes later'
            else:
                content[pk] = 'Checkouts are clear. Youre are welcome!'

        return Response(content)


class ChangeAnyWorkerOfCheckoutListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        checkout = Checkout.objects.filter(id=pk).first()

        checkouts = Checkout.objects.filter(shop=checkout.shop)
        workers = [x.id for x in Worker.objects.filter(shop=checkout.shop)]
        working_workers = [x.worker.id for x in checkouts]
        free_workers = list(set(workers) - set(working_workers))

        checkout.worker_id = free_workers[0]

        return Response({'success': 'Worker has changed'})


class RebalanceByShopListView(APIView):
    # authentication_classes = [JWTTokenUserAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        checkouts = Checkout.objects.filter(shop=pk).all()

        for checkout in checkouts:
            checkout1 = CheckoutHistory.objects.filter(checkout=checkout.id).order_by('id').last()
            if checkout1 is not None:
                CheckoutHistory.objects.create(checkout=checkout,
                                               max_load=checkout1.max_load,
                                               cur_load=checkout1.max_load)

        return Response()


class ChangeWorkerOfCheckoutListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        checkout = Checkout.objects.filter(id=pk).first()

        checkout.worker_id = request.data['worker_id']
        return Response({'success': 'Worker has changed'})


class GetWorkerOfCheckoutByCheckoutListView(APIView):
    # authentication_classes = [JWTTokenUserAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        checkout = Checkout.objects.filter(id=pk).first()
        cur_worker = Checkout.objects.filter(id=pk).first().worker
        checkouts = Checkout.objects.filter(shop=checkout.shop)
        workers = Worker.objects.filter(shop=pk)
        working_workers = [x.worker for x in checkouts]
        free_workers = [cur_worker] + (list(set(workers) - set(working_workers)))
        return Response(WorkerSerializer(free_workers, many=True).data)


class ReservationsOfCustomerListView(APIView):

    def get(self, request, pk):
        reservations = Reservation.objects.filter(customer=pk).all().order_by('start_time').reverse()

        return Response(ReservationSerializer(reservations, many=True).data)


class CreateBackup(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTTokenUserAuthentication]

    def get(self, request):
        path = "backups/" + str(str(dt.now()).replace(' ', 'T').replace(':', '_').split('.')[0]) + ".json"
        with open(path, 'w', encoding="utf8") as file:
            management.call_command("dumpdata", stdout=file)
        return Response()


class GetBackups(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTTokenUserAuthentication]

    def get(self, request):
        backups = [file.split('.')[0] for file in os.listdir("backups/")]
        return Response(backups)


class RestoreBackup(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTTokenUserAuthentication]

    def get(self, request, pk):
        backups = {index: file for index, file in enumerate(os.listdir("backups/"))}
        print(backups)
        path = "backups/" + str(backups[pk])
        management.call_command("loaddata", path)
        return Response()


class RestoreLastBackup(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTTokenUserAuthentication]

    def get(self, request):
        backups = {index: file for index, file in enumerate(os.listdir("backups/"))}
        print(backups)
        path = "backups/" + backups[len(backups) - 1]
        management.call_command("loaddata", path)
        return Response()
