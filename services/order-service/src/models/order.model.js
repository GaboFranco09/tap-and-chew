const mongoose = require('mongoose');

const orderItemSchema = new mongoose.Schema({
    product_id:  { type: String, required: true },
    name:        { type: String, required: true },
    quantity:    { type: Number, required: true, min: 1 },
    unit_price:  { type: Number, required: true, min: 0 },
}, { _id: false });

const orderSchema = new mongoose.Schema({
    kiosk_id: { type: String, required: true },
    items:    { type: [orderItemSchema], required: true },
    notes:    { type: String, default: '' },
    status:   {
        type:    String,
        enum:    ['pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled'],
        default: 'pending',
    },
    total: { type: Number, required: true, min: 0 },
}, { timestamps: true });

module.exports = mongoose.model('Order', orderSchema);