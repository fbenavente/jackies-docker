import json
import arrow
import random
import string
from mailin import Mailin
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.shortcuts import render, redirect
from management.views import ProductList2
from management.models import (
    Order,
    Product,
    Flavor,
    Size,
    ProductInOrder,
    CustomUser
)
from django.views.decorators.csrf import csrf_exempt


INTEGER_PRODUCT_QTY = [1, 2, 3, 4]
FLOAT_PRODUCT_QTY = [0.5, 1.0, 2.0, 3.0, 4.0]


class SugarFreeProductSerializer(object):
    _flavors = None

    VALID_SIZE_IDS = [16, 6, 8]

    @property
    def flavors(self):
        if not self._flavors:
            flavors_ids = Product.objects.filter(is_sugar_free=True).distinct('flavor_id').values_list('flavor_id', flat=True)
            # flavors
            flavors = []
            for flavor in Flavor.objects.filter(category_id=10, id__in=flavors_ids).order_by('name'):
                flavors.append({'name': flavor.name, 'id': flavor.id})
            self._flavors = flavors
        return self._flavors

    @property
    def price_data(self):
        price_data = {}
        for flavor in self.flavors:
            for size in self.VALID_SIZE_IDS:
                if not price_data.get(flavor['id']):
                    price_data[flavor['id']] = {}
                if not price_data[flavor['id']].get(size):
                    price_data[flavor['id']][size] = None

                try:
                    product = Product.objects.get(category_id=10, flavor_id=flavor['id'], size_id=size, is_sugar_free=True)
                    price_data[flavor['id']][size] = {
                        'price': product.price,
                        'id': product.id,
                        'image': static('media/' + str(product.image)),
                        'size': product.size_name,
                        'flavor': product.flavor_name
                    }
                except Exception as e:
                    print(e)
                    price_data[flavor['id']][size] = {
                        'price': 'NON-EXISTING',
                        'id': '',
                        'image': '',
                        'size': '',
                        'flavor': ''
                    }
        return price_data

    @property
    def sizes(self):
        sizes = []
        size_ids = [16, 6, 8]
        for size in Size.objects.filter(id__in=size_ids):
            sizes.append({
                'id': size.id,
                'name': size.name
            })
        return sizes

    @property
    def data(self):
        return {
            'price_data': self.price_data,
            'flavors': self.flavors,
            'sizes': self.sizes
        }

# TODO: temporal
def autologin(request):
    username = 'pedidos@jackies.cl'
    password = 'jackies55'
    user = authenticate(username=username, password=password)
    do_login(request, user)
    return redirect('pos_orders')


@csrf_exempt
@login_required(login_url='/pos/login/')
def change_order_status(request):
    new_order_status = request.POST.get('new_order_status')
    order_id = request.POST.get('order_id')
    order = Order.objects.get(pk=order_id)
    if new_order_status:
        order.status = int(new_order_status)
        order.save()
    return redirect('pos_orders')


@csrf_exempt
def real_cart(request):
    return render(
        request,
        'landing/landing_order.html'
    )


@csrf_exempt
@login_required(login_url='/pos/login/')
def checkout(request):
    cart_list = json.loads(request.POST.get('cart_list'))
    total = 0
    for cart_item in cart_list:
        total += int(float(cart_item['product_price']) * float(cart_item['product_quantity']))

    # create order first
    order = Order.objects.create(
        order_time=arrow.utcnow().datetime,
        retire_time=arrow.utcnow().datetime,
        order_source=3,
        status=2,
        total=total
    )
    # create products in order
    for cart_item in cart_list:
        product = Product.objects.get(pk=int(cart_item['product_id']))
        ProductInOrder.objects.create(
            order=order,
            product=product,
            quantity=cart_item['product_quantity'],
            subtotal=int(float(cart_item['product_price'])*float(cart_item['product_quantity']))
        )

    return redirect('pos_orders')


def create_order_for_user(cart_list, retire_time, retire_hour, order_comments, user, order_source):
    total = 0
    for cart_item in cart_list:
        total += int(float(cart_item['product_price']) * float(cart_item['product_quantity']))

    # create order first
    retire_time = arrow.get(retire_time, 'DD/MM/YYYY')
    retire_time = retire_time.replace(hour=int(retire_hour))
    order = Order.objects.create(
        order_time=arrow.utcnow().datetime,
        retire_time=retire_time.datetime,
        order_source=order_source,
        status=1,
        user=user,
        comments=order_comments,
        total=total
    )
    # create products in order
    for cart_item in cart_list:
        product = Product.objects.get(pk=int(cart_item['product_id']))
        ProductInOrder.objects.create(
            order=order,
            product=product,
            quantity=cart_item['product_quantity'],
            subtotal=int(float(cart_item['product_price']) * float(cart_item['product_quantity']))
        )
    return order


@csrf_exempt
@login_required(login_url='/pos/login/')
def checkout_new_order(request):
    client_selection = request.POST.get("client_selection")
    if client_selection == 'NEW':
        # create fake default email and password
        random_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        user = CustomUser.objects.create_user(
            email='non_existing_{}@internal.com'.format(random_token),
            password=random_token,
            confirm_password=random_token,
            full_name=request.POST.get("client_full_name"),
            phone_number=request.POST.get("client_phone_number")

        )
    else:  # get User
        user = CustomUser.objects.get(pk=request.POST.get("client_selection"))

    cart_list = json.loads(request.POST.get('cart_list'))
    retire_time = request.POST.get('retire_time')
    retire_hour = request.POST.get('retire_hour').split(":")[0]
    order_comments = request.POST.get('comments')
    create_order_for_user(cart_list, retire_time, retire_hour, order_comments, user, 2)
    return redirect('pos_orders')


@csrf_exempt
@login_required(login_url='/pos/login/')
def edit_order(request):
    order_id = request.POST.get('order_id')
    comments = request.POST.get('comments')
    order = Order.objects.get(id=order_id)
    order.comments = comments
    order.save()
    return redirect('pos_orders')


@csrf_exempt
@login_required(login_url='/pos/login/')
def confirm_order(request):
    cart_list = json.loads(request.POST.get('cart_list'))
    # get order from data
    order_id = request.POST.get('order_id')
    order = Order.objects.get(id=order_id)

    total = 0
    for cart_item in cart_list:
        total += int(float(cart_item['product_price']) * float(cart_item['product_quantity']))

    if total == order.total:  # assuming no changes required
        print ("Same total")
    else:
        print ("removing all...")
        # remove all product in Order and add the news
        ProductInOrder.objects.filter(order_id=order_id).delete()
        # create products in order
        for cart_item in cart_list:
            product = Product.objects.get(pk=int(cart_item['product_id']))
            ProductInOrder.objects.create(
                order=order,
                product=product,
                quantity=cart_item['product_quantity'],
                subtotal=int(float(cart_item['product_price'])*float(cart_item['product_quantity']))
            )
    order.status = 2  # delivered
    order.total = total
    order.save()
    return redirect('pos_orders')


@csrf_exempt
@login_required(login_url='/pos/login/')
def order(request, order_id):
    # order = Order.objects.filter(id=order_id)
    # order = order[0]
    order_products = []
    for order_product in ProductInOrder.objects.filter(order_id=order_id):
        product = order_product.product

        if product.size:
            if product.is_sugar_free:
                product_desc = "(SIN AZÚCAR) {} | {} (pedido Nº{})".format(product.flavor, product.size.name, order_product.order_id)
            else:
                product_desc = "{} | {} (pedido Nº{})".format(product.flavor, product.size.name, order_product.order_id)
        else:
            if product.is_sugar_free:
                product_desc = "{} | (pedido Nº{})".format(product.flavor, order_product.order_id)
            else:
                product_desc = "{} | (pedido Nº{})".format(product.flavor, order_product.order_id)

        if product.flavor:
            product_flavor = product.flavor.name
        else:
            product_flavor = ''

        if product.size:
            product_size = product.size.name
        else:
            product_size = ''

        product_params = {
            'product_desc': product_desc,
            'product_flavor': product_flavor,
            'product_id': str(product.id),
            'product_name': product.category.name,
            'product_price': str(product.price),
            'product_quantity': str(float(order_product.quantity)),
            'product_size': product_size
        }
        order_products.append(product_params)

    order = Order.objects.get(pk=order_id)

    data_dict = ProductList2().get(request=request).data

    product_families = [
        "torta_de_panqueque",
        "torta",
        "brownies",
        "queque",
        "galletas",
        "pan_de_pascua",
        "merenguitos",
        "kuchen",
        "garrapinadas",
        "productos_especiales"
    ]

    return render(
        request,
        'pos/order.html',
        context={
            'order_products': json.dumps(order_products),
            'order_id': order_id,
            'order': order,
            'data': data_dict,
            'comments': order.comments or '',
            'data_as_json': json.dumps(data_dict),
            'integer_product_qty': INTEGER_PRODUCT_QTY,
            'float_product_qty': FLOAT_PRODUCT_QTY,
            'product_families': product_families,
            'sugar_free_data': SugarFreeProductSerializer().data
        }
    )


def login(request):
    if request.method == 'GET':
        return render(request, 'pos/login.html')

    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        do_login(request, user)
        return redirect('pos_orders')
    else:
        return render(
            request,
            'pos/login.html'
        )


@csrf_exempt
@login_required(login_url='/pos/login/')
def orders(request):
    orders = Order.objects.filter(status__in=[1, 4, 5]).order_by('retire_time')

    # list open orders, all the column sortables, search by RUT, Name, Email, filter by phone or and internet
    # ID
    # deliver_today -> Color
    # Cliente
    # Pedido el order_time
    # Retiro el retire_time
    # filtrar los que hoy se entregan
    # telefono/internet order_source
    # precio total
    # producto y/o productos

    context = {
        'orders': orders
    }
    return render(
        request,
        'pos/orders.html',
        context=context
    )


@csrf_exempt
@login_required(login_url='/pos/login/')
def sale(request):
    data_dict = ProductList2().get(request=request).data

    product_families = [
        "torta_de_panqueque",
        "torta",
        "brownies",
        "queque",
        "galletas",
        "pan_de_pascua",
        "merenguitos",
        "kuchen",
        "garrapinadas",
        "productos_especiales",
        "cajita_de_brownies",
        "paquete_navideno"
    ]

    return render(
        request,
        'pos/sale.html',
        context={
            'data': data_dict,
            'data_as_json': json.dumps(data_dict),
            'product_families': product_families,
            'integer_product_qty': INTEGER_PRODUCT_QTY,
            'float_product_qty': FLOAT_PRODUCT_QTY,
            'sugar_free_data': SugarFreeProductSerializer().data
        }
    )


@csrf_exempt
@login_required(login_url='/pos/login/')
def new_order(request):
    data_dict = ProductList2().get(request=request).data

    product_families = [
        "torta_de_panqueque",
        "torta",
        "brownies",
        "queque",
        "galletas",
        "pan_de_pascua",
        "merenguitos",
        "kuchen",
        "garrapinadas",
        "productos_especiales",
        "cajita_de_brownies",
        "paquete_navideno"

    ]

    available_users = CustomUser.objects.filter(is_admin=False, is_active=True).exclude(id=6)
    return render(
        request,
        'pos/new_order.html',
        context={
            'data': data_dict,
            'retire_hours': [x for x in range(10, 21)],
            'data_as_json': json.dumps(data_dict),
            'product_families': product_families,
            'integer_product_qty': INTEGER_PRODUCT_QTY,
            'float_product_qty': FLOAT_PRODUCT_QTY,
            'available_users': available_users,
            'sugar_free_data': SugarFreeProductSerializer().data
        }
    )


def web_order(request):
    # 4 sabores, 11 diabetica, maracuya-manjar, chocolate guinda
    BLACKLIST_FLAVORS = [
        11,
        13,
        35,
        53,
        52,
        51,
        25,  # limon
        30   # limon-frambuesa
    ]
    VALID_SIZE_IDS = [16, 6, 8, 13]
    # flavors
    flavors = []
    for flavor in Flavor.objects.filter(category_id=10).order_by('name'):
        if int(flavor.id) in BLACKLIST_FLAVORS:
            continue
        flavors.append({'name': flavor.name, 'id': flavor.id})

    default_flavor = request.GET.get('default_flavor', 43)
    default_size = request.GET.get('default_size', 8)

    price_data = {}
    # fill flavors, TODO: move to serializer

    for flavor in flavors:
        if int(flavor['id']) in BLACKLIST_FLAVORS:
            continue
        for size in VALID_SIZE_IDS:
            if not price_data.get(flavor['id']):
                price_data[flavor['id']] = {}
            if not price_data[flavor['id']].get(size):
                price_data[flavor['id']][size] = None

            try:
                product = Product.objects.get(category_id=10, flavor_id=flavor['id'], size_id=size, is_sugar_free=False)
                price_data[flavor['id']][size] = {
                    'price': product.price,
                    'id': product.id,
                    'image': static('media/' + str(product.image))
                }
            except Exception as e:
                print ("no found", flavor['id'], flavor['name'], size)
                price_data[flavor['id']][size] = {
                    'price': 'NON-EXISTING',
                    'id': '',
                    'image': ''
                }

    return render(request, 'landing/final_cart.html', context={
        'flavors': flavors,
        'price_data': price_data,
        'default_flavor': default_flavor,
        'default_size': default_size,
    })


def web_checkout(request):
    DEFAULT_RETIRE_HOUR = 10
    # get or create user
    email = request.POST.get("email")
    random_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    try:
        user = CustomUser.objects.get(email=email)
        user.phone_number = request.POST.get("phone_number")
        user.save()
    except:
        user = CustomUser.objects.create_user(
            email=request.POST.get("email"),
            password=random_token,
            confirm_password=random_token,
            full_name=request.POST.get("full_name"),
            phone_number=request.POST.get("phone_number")
        )
    cart_list = json.loads(request.POST.get('cart_list'))
    retire_time = request.POST.get('retire_time')
    retire_hour = DEFAULT_RETIRE_HOUR
    order_comments = request.POST.get('comments') or ''
    order = create_order_for_user(cart_list, retire_time, retire_hour, order_comments, user, 1)

    email_attrs = {
        'FULL_NAME': order.user.full_name,
        'ORDER_ID': order.id,
        'ORDER_DESCRIPTION': order.description,
        'ORDER_RETIRE_TIME': arrow.get(order.retire_time).format('DD/MM/YYYY')
    }

    m = Mailin("https://api.sendinblue.com/v2.0", '3T5swUHYFB7Lp8PM')
    data = {
        "id": 7,
        "to": order.user.email,
        "bcc": "hermosillavenegas@gmail.com",
        "replyto": "pedidos@jackies.cl",
        "attr": email_attrs,
        "headers": {"Content-Type": "text/html;charset=iso-8859-1"}
    }

    result = m.send_transactional_template(data)
    print(result)
    return redirect('post_checkout')


def post_checkout(request):
    return render(request, 'landing/post_checkout.html')
