const Payment = require('../models/payment.model');


// GET /api/payments
const getAllPayments = async (req, res) => {
    try {
        const { status, method } = req.query;
        const filter = {};

        if (status) filter.status = status;
        if (method) filter.payment_method = method;

        const payments = await Payment.find(filter).sort({ createdAt: -1 });
        res.json(payments);
    } catch (error) {
        res.status(500).json({ message: 'Error al obtener pagos.', error: error.message });
    }
};


// GET /api/payments/:id
const getPaymentById = async (req, res) => {
    try {
        const payment = await Payment.findById(req.params.id);
        if (!payment) return res.status(404).json({ message: 'Pago no encontrado.' });
        res.json(payment);
    } catch (error) {
        res.status(500).json({ message: 'Error al obtener pago.', error: error.message });
    }
};


// GET /api/payments/order/:order_id
const getPaymentByOrder = async (req, res) => {
    try {
        const payment = await Payment.findOne({ order_id: req.params.order_id });
        if (!payment) return res.status(404).json({ message: 'Pago no encontrado para este pedido.' });
        res.json(payment);
    } catch (error) {
        res.status(500).json({ message: 'Error al obtener pago.', error: error.message });
    }
};


// POST /api/payments
const createPayment = async (req, res) => {
    try {
        const { order_id, kiosk_id, items, subtotal, discount, tip, total, payment_method, notes } = req.body;

        const existing = await Payment.findOne({ order_id });
        if (existing) return res.status(409).json({ message: 'Este pedido ya tiene un pago registrado.' });

        const payment = new Payment({
            order_id,
            kiosk_id,
            items,
            subtotal,
            discount: discount || 0,
            tip:      tip || 0,
            total,
            payment_method,
            notes:    notes || '',
            status:   'completed',
        });

        await payment.save();

        res.status(201).json({
            message:        'Pago registrado exitosamente.',
            payment,
        });
    } catch (error) {
        res.status(500).json({ message: 'Error al registrar pago.', error: error.message });
    }
};


// PATCH /api/payments/:id/refund
const refundPayment = async (req, res) => {
    try {
        const payment = await Payment.findById(req.params.id);
        if (!payment) return res.status(404).json({ message: 'Pago no encontrado.' });

        if (payment.status === 'refunded') {
            return res.status(409).json({ 
                message: 'Este pago ya fue reembolsado.' 
            });
        }

        if (payment.status !== 'completed') {
            return res.status(409).json({ message: 'Solo se pueden reembolsar pagos completados.' });
        }



        payment.status = 'refunded';
        await payment.save();

        res.json({ message: 'Reembolso procesado.', payment });
    } catch (error) {
        res.status(500).json({ message: 'Error al procesar reembolso.', error: error.message });
    }
};


// GET /api/payments/stats
const getStats = async (req, res) => {
    try {
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const stats = await Payment.aggregate([
            { $match: { createdAt: { $gte: today }, status: 'completed' } },
            {
                $group: {
                    _id:            null,
                    total_revenue:  { $sum: '$total' },
                    total_orders:   { $count: {} },
                    avg_ticket:     { $avg: '$total' },
                }
            }
        ]);

        const byMethod = await Payment.aggregate([
            { $match: { createdAt: { $gte: today }, status: 'completed' } },
            { $group: { _id: '$payment_method', count: { $count: {} }, total: { $sum: '$total' } } }
        ]);

        res.json({
            today:     stats[0] || { total_revenue: 0, total_orders: 0, avg_ticket: 0 },
            by_method: byMethod,
        });
    } catch (error) {
        res.status(500).json({ message: 'Error al obtener estadísticas.', error: error.message });
    }
};

module.exports = {
    getAllPayments,
    getPaymentById,
    getPaymentByOrder,
    createPayment,
    refundPayment,
    getStats,
};