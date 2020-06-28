from django.shortcuts import render
import arrow
import random
from management.models import ProductInOrder, Order, Product
from django.db.models import Sum, Count
from django.db import connection
from django.db.models import Q
from babel.numbers import format_currency
from django.contrib.admin.views.decorators import staff_member_required   

@staff_member_required
def dashboard(request):
    today = arrow.now()
    now = today.floor('month')
    amount_this_month = Order.objects.filter(retire_time__gte=now.datetime, status=2).aggregate(Sum('total'))['total__sum'] or 0.0
    count_this_month = int(ProductInOrder.objects.filter(order__retire_time__gte=now.datetime, order__status=2).aggregate(Sum('quantity'))['quantity__sum'] or 0)
    open_now = Order.objects.filter(retire_time__gte=now.datetime, status__in=[1, 4, 5]).aggregate(Count('total'))['total__count']
    
    # internet information
    internet_sales_count = Order.objects.filter(retire_time__gte=now.datetime, order_source=1, status=2).aggregate(Count('total'))['total__count']
    no_internet_sales_count = Order.objects.filter(retire_time__gte=now.datetime, status=2).exclude(order_source=1).aggregate(Count('total'))['total__count']

    count_compared_with_no_internet_percentage = 0
    if no_internet_sales_count:
        count_compared_with_no_internet_percentage = int((internet_sales_count * 100) / no_internet_sales_count)

    # last 5 sales
    last_5_sales = Order.objects.filter(status=2).order_by('-id')[:5]

    # comparison with last year
    last_year_ceil = today.shift(years=-1)
    last_year_floor = last_year_ceil.floor('month')
    # amount
    amount_last_year = Order.objects.filter(retire_time__gte=last_year_floor.datetime, retire_time__lte=last_year_ceil.datetime, status=2).aggregate(Sum('total'))['total__sum']
    # count
    count_last_year = int(ProductInOrder.objects.filter(order__retire_time__gte=last_year_floor.datetime, order__retire_time__lte=last_year_ceil.datetime, order__status=2).aggregate(Sum('quantity'))['quantity__sum'])

    # percentage last year count
    if count_this_month > count_last_year:
        is_count_compared_with_last_year_greater = True
        count_compared_with_last_year_percentage = 100 - int((count_last_year * 100) / count_this_month)
    else:
        is_count_compared_with_last_year_greater = False
        count_compared_with_last_year_percentage = 100 - int((count_this_month * 100) / count_last_year)

    # percentage last year amount
    if amount_this_month > amount_last_year:
        is_amount_compared_with_last_year_greater = True
        amount_compared_with_last_year_percentage = 100 - int((amount_last_year * 100) / amount_this_month)
    else:
        is_amount_compared_with_last_year_greater = False
        amount_compared_with_last_year_percentage = 100 - int((amount_this_month * 100) / amount_last_year)

    open_orders  = Order.objects.filter(status__in=[1, 4, 5]).order_by('retire_time')

    context = {
        'amount_this_month': format_currency(amount_this_month, 'CLP', locale='es_CL'),
        'count_this_month': count_this_month,
        'open_now': open_now,
        'open_orders': open_orders,
        'internet_sales_count': internet_sales_count,
        'last_5_sales': last_5_sales,
        'count_last_year': count_last_year,
        'count_compared_with_no_internet_percentage': count_compared_with_no_internet_percentage,
        'is_count_compared_with_last_year_greater': is_count_compared_with_last_year_greater,
        'count_compared_with_last_year_percentage': count_compared_with_last_year_percentage,
        'is_amount_compared_with_last_year_greater': is_amount_compared_with_last_year_greater,
        'amount_compared_with_last_year_percentage': amount_compared_with_last_year_percentage
    }

    # numero de pedidos pendientes
    return render(
        request,
        'dashboard/dashboard.html',
        context=context
    )

@staff_member_required
def sales_by_year(request):
    return render(
        request,
        'dashboard/per_year.html',
        context = {'per_year': YearSalesMoney(arrow.now().shift(years=-4), arrow.now()).data}
    )


@staff_member_required
def sales_by_sku(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    if from_date:
        from_date = arrow.get(from_date, 'DD/MM/YYYY').to('America/Santiago').floor('day')
    else:
        from_date = arrow.utcnow().shift(months=-1).floor('day')
    if to_date:
        to_date = arrow.get(to_date, 'DD/MM/YYYY').to('America/Santiago').ceil('day')
    else:
        to_date = arrow.utcnow().ceil('day')
    by_amount = BySKU(from_date, to_date)
    total = sum([x['total'] for x in by_amount.data['datasets']])
    count = sum([x['count'] for x in by_amount.data['datasets']])
    return render(
        request,
        'dashboard/per_sku.html',
        context={
            'by_amount': by_amount.data,
            'total': total,
            'count': count,
            'from_date': from_date.format('DD/MM/YYYY'),
            'to_date': to_date.format('DD/MM/YYYY')
        }
    )

@staff_member_required
def sales_by_type(request):
    per_flavor = PerProductFlavorUnits()
    per_size = PerProductSizeUnits()
    return render(
        request,
        'dashboard/per_type.html',
        context = {
            'per_flavor': per_flavor.data,
            'per_size': per_size.data
        }
    )

@staff_member_required
def sales(request):
    m = MonthlySalesMoney(arrow.now().shift(months=-12), arrow.now())
    u = MonthlySalesUnits(arrow.now().shift(months=-12), arrow.now())
    return render(
        request,
        'dashboard/sales.html',
        context = {'monthly_amounts': m.data, 'monthly_units': u.data}
    )


class PerProductFlavorUnits(object):
    @property
    def data(self):
        data = {'labels': [], 'datasets': [{'label': "XYZ", 'backgroundColor': [], 'data': []}]}
        q = ProductInOrder.objects.filter(product__category_id=10).values('product__flavor__name', 'product__flavor_id').annotate(total=Count('product__flavor_id')).order_by('total')
        for r in q:
            color = lambda: random.randint(0,255) 
            data['labels'].append(r['product__flavor__name'])
            data['datasets'][0]['backgroundColor'].append('#%02X%02X%02X' % (color(),color(),color()))
            data['datasets'][0]['data'].append(r['total'])
        return data


class PerProductSizeUnits(object):
    @property
    def data(self):
        data = {'labels': [], 'datasets': [{'label': "XYZ", 'backgroundColor': [], 'data': []}]}
        q = ProductInOrder.objects.filter(product__category_id=10).values('product__size__name', 'product__size_id').annotate(total=Count('product__size_id')).order_by('total')
        for r in q:
            color = lambda: random.randint(0,255) 
            data['labels'].append(r['product__size__name'])
            data['datasets'][0]['backgroundColor'].append('#%02X%02X%02X' % (color(),color(),color()))
            data['datasets'][0]['data'].append(r['total'])
        return data


class BySKU(object):
    def __init__(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date

    @property
    def datasets(self):
        # group by product
        q = ProductInOrder.objects.filter(
            order__retire_time__gte=self.from_date.datetime,
            order__retire_time__lte=self.to_date.datetime,
            order__status=2
        ).values('order__product').annotate(total=Sum('subtotal'), count=Sum('quantity')).order_by('total')
        results = []
        for r in q:
            if r['total'] == 0 or not r['total']:
                continue
            product = Product.objects.get(pk=r['order__product'])
            results.append({
                'id': r['order__product'],
                'count': r['count'],
                'size': product.size_name,
                'flavor': product.flavor_name,
                'category': product.category_name,
                'total': r['total']
            })
        return results

    @property
    def data(self):
        return {'datasets': self.datasets}


class BySKUCount(object):
    def __init__(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date

    @property
    def datasets(self):
        # group by product
        q = ProductInOrder.objects.filter(
            order__retire_time__gte=self.from_date.datetime,
            order__retire_time__lte=self.to_date.datetime,
            status=2
        ).values('order__product').annotate(total=Count('id')).order_by('-total')
        results = []
        for r in q:
            if r['total'] == 0 or not r['total']:
                continue
            product = Product.objects.get(pk=r['order__product'])
            results.append({
                'id': r['order__product'],
                'size': product.size_name,
                'flavor': product.flavor_name,
                'category': product.category_name,
                'total': r['total']
            })
        return results


    @property
    def data(self):
        return {'datasets': self.datasets}


class MonthlySalesMoney(object):
    def __init__(self, from_date=None, to_date=None):
        self.from_date = from_date
        self.to_date = to_date

    @property
    def labels(self):
        labels = []
        for floor, _ in arrow.Arrow.span_range('month', self.from_date, self.to_date):
            labels.append(floor.format('MM/YYYY'))
        return labels

    @property
    def datasets(self):
        datasets = [
            {
                'label': 'Torta panqueque',
                'backgroundColor': "#f9c00c",
                'data': [],
            },
            {
                'label': 'Torta',
                'backgroundColor': "#00b9f1",
                'data': [],
            },
            {
                'label': 'Brownie',
                'backgroundColor': "#7200da",
                'data': [],
            },
            {
                'label': 'Queque',
                'backgroundColor': "#f9320c",
                'data': [],
            },
            {
                'label': 'Galletas',
                'backgroundColor': "#75D701",
                'data': [],
            }
        ]

        for from_on_month, to_on_month in arrow.Arrow.span_range('month', self.from_date, self.to_date):
            total_panqueque = ProductInOrder.objects.filter(
                order__retire_time__gte=from_on_month.datetime,
                order__retire_time__lte=to_on_month.datetime,
                order__status=2,
                product__category_id=10
            ).aggregate(Sum('subtotal'))

            total_torta = ProductInOrder.objects.filter(
                order__retire_time__gte=from_on_month.datetime,
                order__retire_time__lte=to_on_month.datetime,
                order__status=2,
                product__category_id=9
            ).aggregate(Sum('subtotal'))

            total_brownie = ProductInOrder.objects.filter(
                order__retire_time__gte=from_on_month.datetime,
                order__retire_time__lte=to_on_month.datetime,
                order__status=2,
                product__category_id=1
            ).aggregate(Sum('subtotal'))

            total_queque = ProductInOrder.objects.filter(
                order__retire_time__gte=from_on_month.datetime,
                order__retire_time__lte=to_on_month.datetime,
                order__status=2,
                product__category_id=7
            ).aggregate(Sum('subtotal'))

            total_galletas = ProductInOrder.objects.filter(
                order__retire_time__gte=from_on_month.datetime,
                order__retire_time__lte=to_on_month.datetime,
                order__status=2,
                product__category_id=2
            ).aggregate(Sum('subtotal'))
            
            datasets[0]['data'].append(total_panqueque['subtotal__sum'] or 0)
            datasets[1]['data'].append(total_torta['subtotal__sum'] or 0)
            datasets[2]['data'].append(total_brownie['subtotal__sum'] or 0)
            datasets[3]['data'].append(total_queque['subtotal__sum'] or 0)
            datasets[4]['data'].append(total_galletas['subtotal__sum'] or 0)

        return datasets

    @property
    def data(self):
        return {
            'labels': self.labels,
            'datasets': self.datasets
        }

class MonthlySalesUnits(object):
    def __init__(self, from_date=None, to_date=None):
        self.from_date = from_date
        self.to_date = to_date

    @property
    def labels(self):
        labels = []
        for floor, _ in arrow.Arrow.span_range('month', self.from_date, self.to_date):
            labels.append(floor.format('MM/YYYY'))
        return labels

    @property
    def datasets(self):
        datasets = [
            {
                'label': 'Torta panqueque',
                'backgroundColor': "#f9c00c",
                'data': [],
            },
            {
                'label': 'Torta',
                'backgroundColor': "#00b9f1",
                'data': [],
            },
            {
                'label': 'Brownie',
                'backgroundColor': "#7200da",
                'data': [],
            },
            {
                'label': 'Queque',
                'backgroundColor': "#f9320c",
                'data': [],
            },
            {
                'label': 'Galletas',
                'backgroundColor': "#75D701",
                'data': [],
            }
        ]

        for from_on_month, to_on_month in arrow.Arrow.span_range('month', self.from_date, self.to_date):
            total_panqueque = ProductInOrder.objects.filter(
                order__retire_time__gte=from_on_month.datetime,
                order__retire_time__lte=to_on_month.datetime,
                order__status=2,
                product__category_id=10
            ).aggregate(Sum('quantity'))

            total_torta = ProductInOrder.objects.filter(
                order__retire_time__gte=from_on_month.datetime,
                order__retire_time__lte=to_on_month.datetime,
                order__status=2,
                product__category_id=9
            ).aggregate(Sum('quantity'))

            total_brownie = ProductInOrder.objects.filter(
                order__retire_time__gte=from_on_month.datetime,
                order__retire_time__lte=to_on_month.datetime,
                order__status=2,
                product__category_id=1
            ).aggregate(Sum('quantity'))

            total_queque = ProductInOrder.objects.filter(
                order__retire_time__gte=from_on_month.datetime,
                order__retire_time__lte=to_on_month.datetime,
                order__status=2,
                product__category_id=7
            ).aggregate(Sum('quantity'))

            total_galletas = ProductInOrder.objects.filter(
                order__retire_time__gte=from_on_month.datetime,
                order__retire_time__lte=to_on_month.datetime,
                order__status=2,
                product__category_id=2
            ).aggregate(Sum('quantity'))

            datasets[0]['data'].append(int(total_panqueque['quantity__sum'] or 0))
            datasets[1]['data'].append(int(total_torta['quantity__sum'] or 0))
            datasets[2]['data'].append(int(total_brownie['quantity__sum' or 0]))
            datasets[3]['data'].append(int(total_queque['quantity__sum'] or 0))
            datasets[4]['data'].append(int(total_galletas['quantity__sum'] or 0))
        return datasets

    @property
    def data(self):
        return {
            'labels': self.labels,
            'datasets': self.datasets
        }


class YearSalesMoney(object):
    def __init__(self, from_date=None, to_date=None):
        self.from_date = from_date
        self.to_date = to_date

    @property
    def labels(self):
        labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        return labels

    @property
    def datasets(self):

        color_set = [
            '#f9c00c',
            '#00b9f1',
            '#7200da',
            '#f9320c',
            '#34314c'
        ]
        selected_color = 0

        datasets = []
        for from_on_year, to_on_year in arrow.Arrow.span_range('year', self.from_date, self.to_date):
            color = color_set[selected_color]
            selected_color += 1 
            dataset = {
                'label': from_on_year.format('YYYY'),
                'borderColor': color,
                'data': [],
            }
            for from_on_month, to_on_month in arrow.Arrow.span_range('month', from_on_year, to_on_year):
                total = Order.objects.filter(
                    retire_time__gte=from_on_month.datetime,
                    retire_time__lte=to_on_month.datetime,
                    status=2
                ).aggregate(Sum('total'))
                if total['total__sum']:
                    dataset['data'].append(total['total__sum'] or 0)
            datasets.append(dataset)
        return datasets

    @property
    def data(self):
        return {
            'labels': self.labels,
            'datasets': self.datasets
        }


