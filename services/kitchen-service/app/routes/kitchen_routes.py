from flask import Blueprint
from app.middlewares.internal_auth import internal_auth_required
from app.controllers.kitchen_controller import (
    get_queue,
    sync_queue,
    receive_order,
    start_order,
    complete_order,
    toggle_item,
    get_history,
)

kitchen_bp = Blueprint('kitchen', __name__)

# Aplicar middleware a todas las rutas
kitchen_bp.before_request(lambda: internal_auth_required(lambda: None)())


@kitchen_bp.get('/queue')
@internal_auth_required
def queue():
    return get_queue()


@kitchen_bp.get('/history')
@internal_auth_required
def history():
    return get_history()


@kitchen_bp.post('/sync')
@internal_auth_required
def sync():
    return sync_queue()


@kitchen_bp.post('/orders')
@internal_auth_required
def receive():
    return receive_order()


@kitchen_bp.patch('/orders/<string:order_id>/start')
@internal_auth_required
def start(order_id):
    return start_order(order_id)


@kitchen_bp.patch('/orders/<string:order_id>/complete')
@internal_auth_required
def complete(order_id):
    return complete_order(order_id)


@kitchen_bp.patch('/orders/<string:order_id>/items/<int:item_id>/toggle')
@internal_auth_required
def toggle(order_id, item_id):
    return toggle_item(order_id, item_id)