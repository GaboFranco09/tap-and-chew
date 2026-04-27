const Notification = require('../models/notification.model');

// GET /api/notifications/order/:order_id
const getByOrder = async (req, res) => {
    try {
        const notifications = await Notification.find({
            order_id: req.params.order_id,
        }).sort({ createdAt: -1 });

        res.json(notifications);
    } catch (error) {
        res.status(500).json({ message: 'Error al obtener notificaciones.', error: error.message });
    }
};

// POST /api/notifications
const create = async (req, res) => {
    try {
        const { order_id, type, message } = req.body;

        if (!order_id || !type || !message) {
            return res.status(400).json({ message: 'order_id, type y message son requeridos.' });
        }

        const notification = new Notification({ order_id, type, message });
        await notification.save();

        res.status(201).json({
            message:      'Notificación creada.',
            notification,
        });
    } catch (error) {
        res.status(500).json({ message: 'Error al crear notificación.', error: error.message });
    }
};

// PATCH /api/notifications/:id/read
const markAsRead = async (req, res) => {
    try {
        const notification = await Notification.findById(req.params.id);
        if (!notification) {
            return res.status(404).json({ message: 'Notificación no encontrada.' });
        }

        notification.is_read = true;
        await notification.save();

        res.json({ message: 'Notificación marcada como leída.', notification });
    } catch (error) {
        res.status(500).json({ message: 'Error al actualizar notificación.', error: error.message });
    }
};

module.exports = { getByOrder, create, markAsRead };