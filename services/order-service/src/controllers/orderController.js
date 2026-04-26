const Order = require('../models/order.model');

// GET /api/orders
const getOrders = async (req, res) => {
    try {
        const filter = {};
        if (req.query.status) filter.status = req.query.status;

        const orders = await Order.find(filter).sort({ createdAt: -1 });
        res.json(orders);
    } catch (error) {
        res.status(500).json({ message: 'Error al obtener pedidos.', error: error.message });
    }
};

// GET /api/orders/status/pending
const getPendingOrders = async (req, res) => {
    try {
        const orders = await Order.find({
            status: { $in: ['pending', 'confirmed'] }
        }).sort({ createdAt: 1 });

        res.json(orders);
    } catch (error) {
        res.status(500).json({ message: 'Error al obtener pedidos pendientes.', error: error.message });
    }
};

// GET /api/orders/:id
const getOrderById = async (req, res) => {
    try {
        const order = await Order.findById(req.params.id);
        if (!order) return res.status(404).json({ message: 'Pedido no encontrado.' });
        res.json(order);
    } catch (error) {
        res.status(500).json({ message: 'Error al obtener pedido.', error: error.message });
    }
};

// POST /api/orders
const createOrder = async (req, res) => {
    try {
        const { kiosk_id, items, notes, total } = req.body;

        if (!kiosk_id || !items || !items.length || !total) {
            return res.status(400).json({ message: 'kiosk_id, items y total son requeridos.' });
        }

        const order = new Order({ kiosk_id, items, notes, total });
        await order.save();

        res.status(201).json({
            message: 'Pedido creado exitosamente.',
            order,
        });
    } catch (error) {
        res.status(500).json({ message: 'Error al crear pedido.', error: error.message });
    }
};

// PATCH /api/orders/:id/status
const updateStatus = async (req, res) => {
    try {
        const { status } = req.body;
        const validStatuses = ['pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled'];

        if (!validStatuses.includes(status)) {
            return res.status(400).json({ message: 'Estado inválido.' });
        }

        const order = await Order.findById(req.params.id);
        if (!order) return res.status(404).json({ message: 'Pedido no encontrado.' });

        if (order.status === 'cancelled') {
            return res.status(409).json({ message: 'No se puede modificar un pedido cancelado.' });
        }

        order.status = status;
        await order.save();

        res.json({ message: 'Estado actualizado.', order });
    } catch (error) {
        res.status(500).json({ message: 'Error al actualizar estado.', error: error.message });
    }
};

// DELETE /api/orders/:id
const cancelOrder = async (req, res) => {
    try {
        const order = await Order.findById(req.params.id);
        if (!order) return res.status(404).json({ message: 'Pedido no encontrado.' });

        if (['preparing', 'ready', 'delivered'].includes(order.status)) {
            return res.status(409).json({
                message: 'No se puede cancelar un pedido en preparación, listo o entregado.',
            });
        }

        order.status = 'cancelled';
        await order.save();

        res.json({ message: 'Pedido cancelado.', order });
    } catch (error) {
        res.status(500).json({ message: 'Error al cancelar pedido.', error: error.message });
    }
};

module.exports = {
    getOrders,
    getPendingOrders,
    getOrderById,
    createOrder,
    updateStatus,
    cancelOrder,
};