from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Permission
from django.db import models
from django.utils import timezone

from authentication.models import UserManager


class Shop(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    open_time = models.FloatField(default=9)
    close_time = models.FloatField(default=21)
    image = models.ImageField(upload_to='shops/', null=True, blank=True)
    url = models.URLField(unique=True)
    commonWaitingTime = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Administrator(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user_permissions = None
    groups = None
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'shop']

    objects = UserManager()

    def __str__(self):
        return f'{self.name} {self.surname}'


class Worker(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_permissions = None
    groups = None
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'shop']

    objects = UserManager()

    def __str__(self):
        return f'{self.name} {self.surname}'


class Checkout(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or self.id


class Customer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    user_permissions = None
    groups = None
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def __str__(self):
        return f'{self.name} {self.surname}\t\t({self.email})'


class CustomerHistory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    start_visit = models.DateTimeField(auto_now_add=False)
    finish_visit = models.DateTimeField(default=timezone.now, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.customer.name} {self.customer.surname}\t\t{self.start_visit} - {self.finish_visit}'


class CheckoutHistory(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    max_load = models.IntegerField(default=2)
    cur_load = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.checkout.title or self.checkout.id}\t\t{self.time}'


class Reservation(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.customer.name} {self.customer.surname}'
