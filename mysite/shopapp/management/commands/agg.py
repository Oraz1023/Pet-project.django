from django.core.management import BaseCommand
from shopapp.models import Product, Order
from django.db.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo aggregate")
        # result = Product.objects.filter(
        #     name__contains="Smartphone").aggregate(
        #     avg_price=Avg("price"),
        #     max_price=Max( "price"),
        #     min_price=Min( "price"),
        #     count=Count( "id"),
        # )
        # print(result)
        orders=Order.objects.annotate(
            total_price=Sum("products__price", default=0),
            products_count=Count("products"),
        )
        for order in orders:
            print(
                f"Order# {order.id}"
                f" with {order.products_count}"
                f" products worth {order.total_price}"
            )
        self.stdout.write("Done")
