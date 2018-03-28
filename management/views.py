from rest_framework.response import Response
from rest_framework import status, generics, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from management.serializers import *
from management.models import *
from management.permissions import IsAccountOwner
from django.shortcuts import render
import logging
import json
from django.contrib.auth import authenticate, login, logout
from _constants.messages import *
from _constants.choices import ORDER_STATUS_CODES, ORDER_SOURCE, PRODUCT_STATUS_CODES
from datetime import datetime
from collections import OrderedDict


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BackgroundList(generics.ListCreateAPIView):
    queryset = Background.objects.all().order_by('?')
    serializer_class = BackgroundSerializer
    pagination_class = LargeResultsSetPagination


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderList(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request):
        """
        This function creates an order object with its associated products
        """

        data = request.data
        # This status is initialized in a error state. If everything is ok should be a valid status
        result_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        if 'order_data' not in data or 'products' not in data:
            logging.info(ERROR_ORDER_DATA_STRUCTURE)
            return Response({'message': ERROR_ORDER_DATA_STRUCTURE}, status=status.HTTP_400_BAD_REQUEST)

        order_data = data.get('order_data',{})
        products = data.get('products', [])

        if not products:
            logging.info(ERROR_PRODUCT_NOT_PROVIDED)
            return Response({'message': ERROR_PRODUCT_NOT_PROVIDED}, status=status.HTTP_400_BAD_REQUEST)

        if 'retire_time' not in order_data:
            logging.info(ERROR_RETIRE_TIME_NOT_PROVIDED)
            return Response({'message': ERROR_RETIRE_TIME_NOT_PROVIDED}, status=status.HTTP_400_BAD_REQUEST)

        if 'discount' not in order_data:
            logging.info(ERROR_DISCOUNT_NOT_PROVIDED)
            return Response({'message': ERROR_DISCOUNT_NOT_PROVIDED}, status=status.HTTP_400_BAD_REQUEST)

        if 'total' not in order_data:
            logging.info(ERROR_TOTAL_NOT_PROVIDED)
            return Response({'message': ERROR_TOTAL_NOT_PROVIDED}, status=status.HTTP_400_BAD_REQUEST)

        order_data["user"] = request.user.id
        order_data["retire_time"] = datetime.strptime(order_data["retire_time"], '%d-%m-%Y:%H')
        if not request.user.is_admin:
            order_data["name"] = request.user.get_full_name()
            order_data["phone_number"] = request.user.phone_number
            order_data["email"] = request.user.email
            order_data["order_source"] = ORDER_SOURCE[0][0]
        else:
            order_data["order_source"] = ORDER_SOURCE[1][0]


        new_order = OrderSerializer(data=order_data)
        if not new_order.is_valid():
            return Response(new_order.errors, status.HTTP_400_BAD_REQUEST)
        new_order.save()

        return Response(new_order, status=status.HTTP_201_CREATED)



class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        # This method returns a dict with three arrays: category, flavor and size for the dropdowns
        data_dict = {"categories": [], "flavors": {}, "sizes": {}, "products":{}}
        flavors_per_category = {}
        sizes_per_flavor_category = {}
        products_dict = OrderedDict()
        #ToDo adding a top 10 filter (most sold)
        products = Product.objects.filter(status=PRODUCT_STATUS_CODES[0][0]).order_by("category", "flavor", "size")
        categories_ids = products.values_list("category", flat=True).distinct("category")
        categories = Category.objects.filter(id__in=categories_ids)

        data_dict["categories"] = CategorySerializer(categories, many=True).data
        for product in products:
            if not product.category.name in products_dict:
                products_dict[product.category.name] = {}
                flavors_per_category[product.category.name] = []
                sizes_per_flavor_category[product.category.name] = {}

            flavor, flavor_image = getFlavorName(product)
            size, size_image = getSizeName(product)

            if not flavor in products_dict[product.category.name]:
                products_dict[product.category.name][flavor] = {}
                if flavor != "":
                    flavors_per_category[product.category.name].append(FlavorSerializer(product.flavor).data)
                else:
                    flavors_per_category[product.category.name].append("")
                sizes_per_flavor_category[product.category.name][flavor] = []

            if size != "":
                sizes_per_flavor_category[product.category.name][flavor].append(SizeSerializer(product.size).data)
            else:
                sizes_per_flavor_category[product.category.name][flavor].append("")

            products_dict[product.category.name][flavor][size] = ProductSerializer(product).data
        data_dict["flavors"] = flavors_per_category
        data_dict["sizes"] = sizes_per_flavor_category
        data_dict["products"] = products_dict
        return Response(data_dict, status=status.HTTP_200_OK)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            CustomUser.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, format=None):
        data = json.loads(request.body.decode('utf-8'))

        email = data.get('email', None)
        password = data.get('password', None)

        account = authenticate(email=email, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = CustomUserSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

    # For render the login teplate html, because we are not using Template as view like we use in register case
    def get(self, request):
        return render(request, 'management/login.html')


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


# Both functions below were made to return the name of the flavor or size including the empty string
def getFlavorName(product):
    if product.flavor:
        return product.flavor.name, product.flavor.get_image_url()
    else:
        return "", ""


def getSizeName(product):
    if product.size:
        return product.size.name, product.size.get_image_url()
    else:
        return "", ""

