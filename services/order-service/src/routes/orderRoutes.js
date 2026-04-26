const router       = require('express').Router();
const internalAuth = require('../middlewares/internalAuth');
const ctrl         = require('../controllers/orderController');

router.use(internalAuth);

router.get  ('/status/pending', ctrl.getPendingOrders);
router.get  ('/',               ctrl.getOrders);
router.post ('/',               ctrl.createOrder);
router.get  ('/:id',            ctrl.getOrderById);
router.patch('/:id/status',     ctrl.updateStatus);
router.delete('/:id',           ctrl.cancelOrder);

module.exports = router;