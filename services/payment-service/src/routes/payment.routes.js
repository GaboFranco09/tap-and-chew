const router    = require('express').Router();
const { body }  = require('express-validator');
const validate  = require('../middlewares/validate');
const ctrl      = require('../controllers/payment.controller');

const paymentRules = [
    body('order_id').notEmpty().withMessage('order_id es requerido.'),
    body('kiosk_id').notEmpty().withMessage('kiosk_id es requerido.'),
    body('items').isArray({ min: 1 }).withMessage('items debe ser un arreglo con al menos un elemento.'),
    body('subtotal').isNumeric().withMessage('subtotal debe ser numérico.'),
    body('total').isNumeric().withMessage('total debe ser numérico.'),
    body('payment_method').isIn(['cash', 'card', 'qr']).withMessage('Método de pago inválido.'),
];

router.get ('/',                    ctrl.getAllPayments);
router.get ('/stats',               ctrl.getStats);
router.get ('/order/:order_id',     ctrl.getPaymentByOrder);
router.get ('/:id',                 ctrl.getPaymentById);
router.post('/', ...paymentRules, validate, ctrl.createPayment);
router.patch('/:id/refund',         ctrl.refundPayment);

module.exports = router;