from django.contrib import admin

# Register your models here.
from mainApp.models import Shop, Administrator, Worker, Checkout, Customer, CustomerHistory, CheckoutHistory, \
    Reservation

admin.site.register(Shop)
admin.site.register(Administrator)
admin.site.register(Worker)
admin.site.register(Checkout)
admin.site.register(Customer)
admin.site.register(CustomerHistory)
admin.site.register(CheckoutHistory)
admin.site.register(Reservation)
