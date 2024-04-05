"""
"""
import logging
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.http import *
from timeit import default_timer
from django.contrib.auth import authenticate, login

from django.views import View
from django.views.generic import *

from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from rest_framework.viewsets import ViewSet, ModelViewSet
from .serializers import ProductSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Product, Order, ProductImage
from .forms import ProductForm, GroupForm
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


log=logging.getLogger(__name__)

@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields = [
        "name",
        "description",
    ]
    filterset_fields = [
        "name",
        "price",
        "description",
        # "discount",
        # "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "description",
        "discount",
    ]

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves product, returns 404 if not found",

        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product, by id not found"),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


# Create your views here.

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 3999),
        ]

        context = {
            "time_running": default_timer(),
            "products": products,
        }
        log.debug("Products for shop index: %s", products)
        log.info("Rendering shop index")
        return render(request, 'shopapp/index.html', context=context)


class GroupListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm,
            "groups": Group.objects.prefetch_related('permissions').all(),

        }
        return render(request, 'shopapp/group-list.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.path)


# class ProductDetailView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         product = get_object_or_404(Product,pk=pk)
#         context = {
#             "product": product,
#         }
#         return render(request,'shopapp/product-detail.html', context=context)

class ProductDetailView(DetailView):
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    template_name = 'shopapp/product-detail.html'
    context_object_name = 'product'


# class ProductListView(TemplateView):
#     template_name = 'shopapp/product-list.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.all()
#         return context


class ProductListView(ListView):
    # model = Product
    template_name = 'shopapp/product-list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated

    model = Product
    fields = "__all__"
    success_url = reverse_lazy("shopapp:product-list")


class ProductUpdateView(UpdateView):
    model = Product
    # fields = "__all__"
    template_name_suffix = "-update-form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse("shopapp:product-detail",
                       kwargs={"pk": self.object.pk}, )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
            return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:product-list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
        .all()
    )


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'view_order'
    queryset = (
        Order.objects.select_related('user').prefetch_related('products')
    )


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})
