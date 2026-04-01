const mongoose = require('mongoose');

const paymentItemSchema = new mongoose.Schema({
    product_id:  { type: String, required: true },
    name:        { type: String, required: true },
    quantity:    { type: Number, required: true },
    unit_price:  { type: Number, required: true },
}, { _id: false });


const paymentSchema = new mongoose.Schema({
    order_id:       { type: String, required: true, unique: true },
    kiosk_id:       { type: String, required: true },
    items:          { type: [paymentItemSchema], required: true },

    subtotal:       { type: Number, required: true },
    discount:       { type: Number, default: 0 },
    tip:            { type: Number, default: 0 },
    total:          { type: Number, required: true },

    payment_method: {
        type:     String,
        enum:     ['cash', 'card', 'qr'],
        required: true
    },

    status: {
        type:    String,
        enum:    ['pending', 'completed', 'failed', 'refunded'],
        default: 'pending'
    },

    receipt_number: { type: String, unique: true },
    notes:          { type: String, default: '' },

}, { timestamps: true });


// Generar número de recibo antes de guardar
paymentSchema.pre('save', function () {
    if (!this.receipt_number) {
        const ts     = Date.now().toString().slice(-6);
        const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
        this.receipt_number = `REC-${ts}-${random}`;
    }
    //next();
});

module.exports = mongoose.model('Payment', paymentSchema);