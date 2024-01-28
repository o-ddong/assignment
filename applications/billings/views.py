import traceback

from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, \
    RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.base.response import operation_success, invaild_required_field, ProductPermissionDenied, \
    ProductNotFound, create_success, not_found_data
from applications.billings.models import Product
from applications.billings.serializers import ProductSerializer


class ProductViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin,
                     UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

    def get_object(self, request):
        try:
            product_object = super().get_object()
            if product_object.user == request.user:
                return product_object
            else:
                raise ProductPermissionDenied
        except Exception as e:
            print(traceback.print_exc())
            raise ProductNotFound

    def list(self, request, *args, **kwargs):
        page_size = request.GET.get('size', 10)
        page_no = request.GET.get('page', 1)

        queryset = self.get_queryset()
        paginator = Paginator(queryset, int(page_size))
        page_objs = paginator.get_page(int(page_no))

        serializer = self.serializer_class(page_objs, many=True)

        response = operation_success
        response.data["data"] = serializer.data

        return response

    def create(self, request, *args, **kwargs):
        extra_data = {
            "user": request.user,
            "category": request.data.get('category'),
            "size": request.data.get('size'),
        }
        serializer = self.get_serializer(data=request.data, context={"context": extra_data})
        if serializer.is_valid():
            self.perform_create(serializer)
            response = create_success
            response.data["data"] = serializer.data
            return response
        else:
            print(serializer.errors)
            return invaild_required_field

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object(request)
        serializer = self.get_serializer(instance)

        response = operation_success
        response.data["data"] = serializer.data

        return response

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(request)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response = operation_success
        response.data["data"] = serializer.data

        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(request)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def search(self, request):
        search_name = request.data.get('name')
        if not search_name:
            return invaild_required_field

        product_info = Product.get_matching_products(search_name)
        if not product_info:
            return not_found_data

        serializer = self.get_serializer(product_info)

        response = operation_success
        response.data["data"] = serializer.data

        return response

