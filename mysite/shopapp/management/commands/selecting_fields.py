from typing import Sequence

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from shopapp.models import  Product

# Привязка товаров (Транзакция)
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo select fields")
        users_info=User.objects.values_list("username", flat=True)
        print(list(users_info))
        for user_info in users_info:
            print(user_info)

        paroducts_values=Product.objects.values('pk', 'name')
        for p_values in paroducts_values:
            print(p_values)

        self.stdout.write("Done")