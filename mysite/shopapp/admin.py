from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from .admin_mixins import ExportAsCSVFileMixins

from .models import *


# Register your models here.

class OrderInline(admin.TabularInline):
    model = Product.orders.through


class ProductInline(admin.StackedInline):
    model = ProductImage

@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest,queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description='Unarchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest,queryset: QuerySet):
    queryset.update(archived=False)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVFileMixins):
    actions = [mark_archived,mark_unarchived,'export_csv',]
    inlines = [
        OrderInline,
        ProductInline
               ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount','archived'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = ['name', 'description']
    fieldsets = [
        (None, {
            'fields': ('name', 'description',)
        }),
        ("Price options", {
            'fields': ('price', 'discount'),
            'classes': ('wide', 'collapse'),
        }),
        ("Images",{
            'fields': ('preview',),
        }),
        ("Extra options",{
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': "Extra options. Field 'archived' is for soft delete"
        })]

    def description_short(self, obj: Product) -> str:  # урезание поля descriptions
        if len(obj.description) < 48:
            return obj.description

        return obj.description[:48] + '...'


class ProductInline(admin.StackedInline):
    model = Order.products.through


# admin.site.register(Product, ProductAdmin)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = [mark_archived]
    inlines = [ProductInline]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
