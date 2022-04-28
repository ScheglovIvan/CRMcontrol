#!/usr/bin/env python
from bottle import route, request, run, template # $ pip install bottle

from main import NewOrder, SentOrder


@route('/NewOrder')
def index():
    order_id = request.query.order_id or order_id

    print(order_id)

    NewOrder(order_id)

    print("New order")
    # if NewOrder(order_id):
    #     return template('<b>200</b>')
    # else:
    #     return template('<b>400</b>')

    # return NewOrder(order_id)
    # return template('<b>Create Order: {{order_id}}</b>',
    #                 order_id=order_id)

@route('/SentOrder')
def sent():
    order_id = request.query.order_id or order_id

    print(order_id)

    SentOrder(order_id)

    print("Sent order")

run(host='localhost', port=8000)