from flask import request, jsonify
from app import db
from app.models.kitchen_order import KitchenOrder, KitchenItem
from app.config.firebase import get_db
from datetime import datetime


def get_queue():
    """GET /api/kitchen/queue — todos los pedidos activos en cocina"""
    orders = KitchenOrder.query.filter(
        KitchenOrder.status.in_(['received', 'preparing'])
    ).order_by(KitchenOrder.received_at.asc()).all()

    return jsonify([o.to_dict() for o in orders])


def receive_order():
    """POST /api/kitchen/orders — recibir pedido desde Order Service"""
    data = request.get_json()

    required = ['order_id', 'kiosk_id', 'items', 'total']
    for field in required:
        if field not in data:
            return jsonify({'message': f'{field} es requerido.'}), 400

    # Verificar que no existe ya
    existing = KitchenOrder.query.filter_by(order_id=data['order_id']).first()
    if existing:
        return jsonify({'message': 'El pedido ya fue recibido.'}), 409

    order = KitchenOrder(
        order_id = data['order_id'],
        kiosk_id = data['kiosk_id'],
        notes    = data.get('notes', ''),
        total    = data['total'],
        status   = 'received',
    )

    for item in data['items']:
        order.items.append(KitchenItem(
            product_id = item['product_id'],
            name       = item['name'],
            quantity   = item['quantity'],
            unit_price = item['unit_price'],
        ))

    db.session.add(order)
    db.session.commit()

    return jsonify({
        'message': 'Pedido recibido en cocina.',
        'order':   order.to_dict()
    }), 201


def start_order(order_id):
    """PATCH /api/kitchen/orders/<order_id>/start"""
    order = KitchenOrder.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({'message': 'Pedido no encontrado.'}), 404

    if order.status != 'received':
        return jsonify({'message': 'El pedido ya está en preparación o listo.'}), 409

    order.status     = 'preparing'
    order.started_at = datetime.utcnow()
    db.session.commit()

    # Actualizar estado en Firebase también
    try:
        firebase_db = get_db()
        firebase_db.reference(f'orders/{order_id}').update({
            'status':     'preparing',
            'updated_at': int(datetime.utcnow().timestamp() * 1000)
        })
    except Exception as e:
        print(f'Firebase update error: {e}')

    return jsonify({'message': 'Preparación iniciada.', 'order': order.to_dict()})


def complete_order(order_id):
    """PATCH /api/kitchen/orders/<order_id>/complete"""
    order = KitchenOrder.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({'message': 'Pedido no encontrado.'}), 404

    if order.status != 'preparing':
        return jsonify({'message': 'El pedido debe estar en preparación para marcarlo listo.'}), 409

    order.status       = 'ready'
    order.completed_at = datetime.utcnow()

    for item in order.items:
        item.is_ready = True

    db.session.commit()

    # Actualizar estado en Firebase
    try:
        firebase_db = get_db()
        firebase_db.reference(f'orders/{order_id}').update({
            'status':     'ready',
            'updated_at': int(datetime.utcnow().timestamp() * 1000)
        })
    except Exception as e:
        print(f'Firebase update error: {e}')

    return jsonify({'message': 'Pedido listo para entregar.', 'order': order.to_dict()})


def toggle_item(order_id, item_id):
    """PATCH /api/kitchen/orders/<order_id>/items/<item_id>/toggle"""
    item = KitchenItem.query.filter_by(
        id=item_id,
    ).join(KitchenOrder).filter(
        KitchenOrder.order_id == order_id
    ).first()

    if not item:
        return jsonify({'message': 'Ítem no encontrado.'}), 404

    item.is_ready = not item.is_ready
    db.session.commit()

    return jsonify({
        'message':  'Ítem actualizado.',
        'item_id':  item_id,
        'is_ready': item.is_ready
    })


def get_history():
    """GET /api/kitchen/history — pedidos completados"""
    orders = KitchenOrder.query.filter_by(
        status='ready'
    ).order_by(KitchenOrder.completed_at.desc()).limit(50).all()

    return jsonify([o.to_dict() for o in orders])