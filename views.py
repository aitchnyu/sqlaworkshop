from flask import jsonify, request

from extensions import session
from models import Person, Order


def orders():
    page = int(request.args.get('page', 1))
    paginator = Order.query.join(Person).add_entity(Person).paginate(page, 5)
    out_orders = []
    for order, person in paginator.items:
        out_orders.append({
            'person': person.name,
            'item': order.name,
            'price': order.price
        })
    return jsonify({
        'page': page,
        'pages': paginator.pages,
        'orders': out_orders
    })