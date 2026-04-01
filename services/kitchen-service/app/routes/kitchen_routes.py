from flask import Blueprint
from app.controllers.kitchen_controller import (
    get_queue,
    receive_order,
    start_order,
    complete_order,
    toggle_item,
    get_history,
)

kitchen_bp = Blueprint('kitchen', __name__)

kitchen_bp.get('/queue')(get_queue)
kitchen_bp.get('/history')(get_history)
kitchen_bp.post('/orders')(receive_order)
kitchen_bp.patch('/orders/<string:order_id>/start')(start_order)
kitchen_bp.patch('/orders/<string:order_id>/complete')(complete_order)
kitchen_bp.patch('/orders/<string:order_id>/items/<int:item_id>/toggle')(toggle_item)