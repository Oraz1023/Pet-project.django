from typing import Sequence

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from shopapp.models import Order, Product


# Привязка товаров (Транзакция)
class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order with products")
        user = User.objects.get(username='oraz')
        products: Sequence[Product] = Product.objects.defer("description", "price", "created_at").all()
        products: Sequence[Product] = Product.objects.only("id",).all()
        order, created = Order.objects.get_or_create(
            delivery_address="ulica Ivanova dom 8",
            promocode="promo5",
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f"Created order  {order}")
