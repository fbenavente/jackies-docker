PRODUCT_STATUS_CODES = (
    (1, 'active'),
    (2, 'inactive'),
    (3, 'internal'),
)

ORDER_STATUS_CODES = (
    (1, 'pending'),
    (2, 'delivered'),  # at_rest
    (3, 'cancelled'),  # at_rest
    (4, 'filled'),
    (5, 'completed'),
)

ORDER_STATUS_CODES_DESC = {
    1: 'Por hacer',
    2: 'Entregado',
    3: 'Cancelado',
    4: 'Rellenado',
    5: 'Completo'
}


ORDER_SOURCE = (
    (1, 'web store'),
    (2, 'management'),
    (3, 'pos'),
)

ORDER_STATUS_DESC = {
    1: 'Internet',
    2: 'Teléfono',
    3: 'Tienda'
}

DECORATION_OPTIONS = (
    (1, 'None'),
    (2, 'Simple'),
    (3, 'Complex'),
    (4, 'Very complex'),
)