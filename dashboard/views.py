from django.shortcuts import render
import arrow
from django.db.models import Sum


def dashboard(request):
    return render(
        request,
        'dashboard/dashboard.html'
    )


def sales(request):
    return render(
        request,
        'dashboard/sales.html'
    )


class MonthlySales(object):
    def __init__(self, from_date=None, to_date=None):
        self.from_date = from_date
        self.to_date = to_date

    @property
    def labels(self):
        labels = []
        for r in arrow.Arrow.span_range('month', self.from_date, self.to_date):
            labels.append(r.format('MM/YYYY'))
        return labels


"""
def _monthly_stats(from_date=None, to_date=None, filter_payment_type=None):
    if filter_payment_type and filter_payment_type not in ['cash', 'other']:
        raise Exception('payment_method_alias must be in cash, other')

    if not from_date and not to_date:  # assume last 12 months
        last_12_months = get_last_12_months()
        from_date = last_12_months[0]
        to_date = last_12_months[-1]

    truncate_date = connection.ops.date_trunc_sql('month', 'created')
    qs = Transaction.objects.filter(created__range=(from_date.datetime, to_date.datetime))
    #  apply extra filter
    if filter_payment_type:
        if filter_payment_type == 'cash':
            qs = qs.filter(payment_method='efectivo')
        else:  # other
            qs = qs.exclude(payment_method__in=['efectivo'])

    qs = qs.extra({'month': truncate_date})
    report = qs.values('month').annotate(Sum('amount'), Count('pk')).order_by('month')
    amount_total = sum(map(lambda x: x['amount__sum'] or 0, report))
    return {'report': report, 'sum': amount_total}
"""
"""
    @property
    def datasets(self):
        truncate_date = connection.ops.date_trunc_sql('month', 'created_at')
        qs = Transaction.objects.filter(order__created_at__range=(self.from_date.datetime, self.to_date.datetime))
        qs = qs.extra({'month': truncate_date})
        report = qs.values('month').annotate(Sum('amount'), Count('pk')).order_by('month')
        amount_total = sum(map(lambda x: x['amount__sum'] or 0, report))
        return {'report': report, 'sum': amount_total}

        for r in arrow.Arrow.span_range('month', self.from_date, self.to_date):
            to_on_month = r.ceil('month')
            from_on_month = r.floor('month')
            total_panqueque = ProductInOrder.objects.filter(
                order__created_at__gte=from_on_month.datetime,
                order__created_at__lte=to_on_month.datetime,
                product__category_id=10
            ).aggregate(Sum('total'))

            total_torta = ProductInOrder.objects.filter(
                order__created_at__gte=from_on_month.datetime,
                order__created_at__lte=to_on_month.datetime,
                product__category_id=9
            ).aggregate(Sum('total'))

            total_brownie = ProductInOrder.objects.filter(
                order__created_at__gte=from_on_month.datetime,
                order__created_at__lte=to_on_month.datetime,
                product__category_id=1
            ).aggregate(Sum('total'))

            total_queque = ProductInOrder.objects.filter(
                order__created_at__gte=from_on_month.datetime,
                order__created_at__lte=to_on_month.datetime,
                product__category_id=7
            ).aggregate(Sum('total'))

            total_galletas = ProductInOrder.objects.filter(
                order__created_at__gte=from_on_month.datetime,
                order__created_at__lte=to_on_month.datetime,
                product__category_id=2
            ).aggregate(Sum('total'))


        datasets: [{
            label: 'Employee',
            backgroundColor: "#caf270",
            data: [12, 59, 5, 56, 58,12, 59, 87, 45],
        }, {
            label: 'Engineer',
            backgroundColor: "#45c490",
            data: [12, 59, 5, 56, 58,12, 59, 85, 23],
        }, {
            label: 'Government',
            backgroundColor: "#008d93",
            data: [12, 59, 5, 56, 58,12, 59, 65, 51],
        }, {
            label: 'Political parties',
            backgroundColor: "#2e5468",
            data: [12, 59, 5, 56, 58, 12, 59, 12, 74],
        }],

    @property
    def data(self):
        return {
            'labels': self.labels,
            'datasets': self.datasets
        }
"""