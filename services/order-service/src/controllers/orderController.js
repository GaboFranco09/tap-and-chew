const db   = require('../config/firebase')
const { v4: uuidv4 } = require('uuid')

const ORDER_STATUSES = {
  PENDING:    'pending',
  CONFIRMED:  'confirmed',
  PREPARING:  'preparing',
  READY:      'ready',
  DELIVERED:  'delivered',
  CANCELLED:  'cancelled',
}

// Calcular total del pedido
const calculateTotal = (items) =>
  items.reduce((sum, item) => sum + item.unit_price * item.quantity, 0)

// POST /api/orders
const createOrder = async (req, res, next) => {
  try {
    const { kiosk_id, items, notes } = req.body
    const orderId = uuidv4()

    const order = {
      id:         orderId,
      kiosk_id,
      items,
      notes:      notes || '',
      status:     ORDER_STATUSES.PENDING,
      total:      calculateTotal(items),
      created_at: Date.now(),
      updated_at: Date.now(),
    }

    await db.ref(`orders/${orderId}`).set(order)

    res.status(201).json({
      message: 'Pedido creado correctamente.',
      order,
    })
  } catch (err) {
    next(err)
  }
}

// GET /api/orders
const getAllOrders = async (req, res, next) => {
  try {
    const { status } = req.query
    const snapshot = await db.ref('orders').once('value')
    const data = snapshot.val()

    if (!data) return res.json([])

    let orders = Object.values(data)

    if (status) {
      orders = orders.filter((o) => o.status === status)
    }

    // Ordenar por fecha de creación descendente
    orders.sort((a, b) => b.created_at - a.created_at)

    res.json(orders)
  } catch (err) {
    next(err)
  }
}

// GET /api/orders/:id
const getOrderById = async (req, res, next) => {
  try {
    const snapshot = await db.ref(`orders/${req.params.id}`).once('value')
    const order = snapshot.val()

    if (!order) {
      return res.status(404).json({ message: 'Pedido no encontrado.' })
    }

    res.json(order)
  } catch (err) {
    next(err)
  }
}

// PATCH /api/orders/:id/status
const updateOrderStatus = async (req, res, next) => {
  try {
    const { status } = req.body

    if (!Object.values(ORDER_STATUSES).includes(status)) {
      return res.status(400).json({
        message: `Estado inválido. Valores permitidos: ${Object.values(ORDER_STATUSES).join(', ')}`,
      })
    }

    const snapshot = await db.ref(`orders/${req.params.id}`).once('value')
    if (!snapshot.val()) {
      return res.status(404).json({ message: 'Pedido no encontrado.' })
    }

    await db.ref(`orders/${req.params.id}`).update({
      status,
      updated_at: Date.now(),
    })

    res.json({
      message: 'Estado actualizado.',
      id:      req.params.id,
      status,
    })
  } catch (err) {
    next(err)
  }
}

// DELETE /api/orders/:id  (solo cancelar, no eliminar físicamente)
const cancelOrder = async (req, res, next) => {
  try {
    const snapshot = await db.ref(`orders/${req.params.id}`).once('value')
    const order = snapshot.val()

    if (!order) {
      return res.status(404).json({ message: 'Pedido no encontrado.' })
    }

    if (order.status === ORDER_STATUSES.PREPARING ||
        order.status === ORDER_STATUSES.READY) {
      return res.status(409).json({
        message: 'No se puede cancelar un pedido que ya está en preparación.',
      })
    }

    await db.ref(`orders/${req.params.id}`).update({
      status:     ORDER_STATUSES.CANCELLED,
      updated_at: Date.now(),
    })

    res.json({ message: 'Pedido cancelado.', id: req.params.id })
  } catch (err) {
    next(err)
  }
}

// GET /api/orders/status/pending  — para la pantalla de cocina
const getPendingOrders = async (req, res, next) => {
  try {
    const snapshot = await db.ref('orders')
      .orderByChild('status')
      .equalTo(ORDER_STATUSES.PENDING)
      .once('value')

    const data = snapshot.val()
    if (!data) return res.json([])

    const orders = Object.values(data)
      .sort((a, b) => a.created_at - b.created_at)

    res.json(orders)
  } catch (err) {
    next(err)
  }
}

module.exports = {
  createOrder,
  getAllOrders,
  getOrderById,
  updateOrderStatus,
  cancelOrder,
  getPendingOrders,
}