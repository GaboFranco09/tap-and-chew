from flask import request, jsonify
from app import db
from app.models.kitchen_order import KitchenOrder, KitchenItem
from app.config.order_client import get_pending_orders, update_order_status
from datetime import datetime


def get_queue():
    """GET /api/kitchen/queue — pedidos activos en cocina."""
    orders = KitchenOrder.query.filter(
        KitchenOrder.status.in_(['received', 'preparing'])
    ).order_by(KitchenOrder.received_at.asc()).all()

    return jsonify([o.to_dict() for o in orders])


def sync_queue():
    """POST /api/kitchen/sync — sincroniza cola desde Order Service."""
    try:
        pending = get_pending_orders()
    except Exception as e:
        return jsonify({'message': f'Error al consultar Order Service: {str(e)}'}), 503

    synced = 0
    for order_data in pending:
        order_id = str(order_data.get('_id') or order_data.get('id', ''))
        if not order_id:
            continue

        existing = KitchenOrder.query.filter_by(order_id=order_id).first()
        if existing:
            continue

        order = KitchenOrder(
            order_id   = order_id,
            kiosk_id   = order_data.get('kiosk_id', ''),
            notes      = order_data.get('notes', ''),
            total      = order_data.get('total', 0),
            status     = 'received',
        )

        for item in order_data.get('items', []):
            order.items.append(KitchenItem(
                product_id = item.get('product_id', ''),
                name       = item.get('name', ''),
                quantity   = item.get('quantity', 1),
                unit_price = item.get('unit_price', 0),
            ))

        db.session.add(order)
        synced += 1

    db.session.commit()

    return jsonify({
        'message': f'{synced} pedidos sincronizados desde Order Service.',
        'synced':  synced,
    })


def receive_order():
    """POST /api/kitchen/orders — recibir pedido directamente."""
    data = request.get_json()

    required = ['order_id', 'kiosk_id', 'items', 'total']
    for field in required:
        if field not in data:
            return jsonify({'message': f'{field} es requerido.'}), 400

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

    # Sincronizar con Order Service
    try:
        update_order_status(order_id, 'preparing')
    except Exception as e:
        print(f'Order Service sync error: {e}')

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

    # Sincronizar con Order Service
    try:
        update_order_status(order_id, 'ready')
    except Exception as e:
        print(f'Order Service sync error: {e}')

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
        'is_ready': item.is_ready,
    })


def get_history():
    """GET /api/kitchen/history — pedidos completados."""
    orders = KitchenOrder.query.filter_by(
        status='ready'
    ).order_by(KitchenOrder.completed_at.desc()).limit(50).all()

    return jsonify([o.to_dict() for o in orders])