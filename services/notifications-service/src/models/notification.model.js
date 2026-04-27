const mongoose = require('mongoose');

const notificationSchema = new mongoose.Schema({
    order_id: { type: String, required: true },
    type: {
        type:     String,
        enum:     ['order_confirmed', 'order_ready', 'payment_processed'],
        required: true,
    },
    message:  { type: String, required: true },
    is_read:  { type: Boolean, default: false },
}, { timestamps: true });

module.exports = mongoose.model('Notification', notificationSchema);